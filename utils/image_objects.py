import cv2
import numpy as np


class ImageObject:
    def __init__(self, area, shape=None, shape3d=None):
        """
        constructor of the image object
        which is an object on field
        :param area: the square root of the area of the object (in squared meters), float
        :param shape: optional, the shape of the object (2d)
        used to test if a recorded object is the object represented by the image object
        :param shape3d: the three dimensional shape of the object
        used to estimate things like the center of the actual object
        """
        self.area = area
        self.shape = shape
        self.shape3d = shape3d

    def distance(self, camera, pipeline, frame=None):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param pipeline: a pipeline that returns a float representing the square root of the area of the object
        (in pixels)
        :param frame: optional, a frame to be used instead of the next image from the camera
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return camera.data.constant * self.area / pipeline(camera.read()[1] if frame is None else frame)

    def location2d(self, camera, pipeline, frame=None):
        """
        calculates the 2d location [x z] between the object and the camera
        :param camera: the camera, can be either Camera or CameraList
        :param pipeline: a pipeline that returns the contour of the object
        :param frame: optional, a frame to be used instead of the next image from the camera
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame = camera.read() if frame is None else frame
        cnt = pipeline(frame)
        d_norm = self.distance_by_contours(camera, cnt)
        m = cv2.moments(cnt)
        frame_center = np.array(frame.shape[:2][::-1]) / 2
        vp = m['m10'] / (m['m00'] + 0.000001), m['m01'] / (m['m00'] + 0.000001)
        x, y = np.array(vp) - frame_center
        alpha = x * camera.view_range / frame_center[0]
        return np.array([np.sin(alpha), np.cos(alpha)]) * d_norm

    def distance_by_contours(self, camera, cnt):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return self.area * camera.constant / np.sqrt(cv2.contourArea(cnt))

    def location2d_by_contours(self, camera, cnt):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame_center = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_center = np.array(frame_center) / 2
        m = cv2.moments(cnt)
        vp = m['m10'] / (m['m00'] + 0.000001), m['m01'] / (m['m00'] + 0.000001)
        x, y = np.array(vp) - frame_center
        alpha = x * camera.view_range / frame_center[0]
        return np.array([np.sin(alpha), np.cos(alpha)]) * self.distance_by_contours(camera, cnt)

    def distance_by_params(self, camera, area):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
        (in pixels)
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return camera.constant * self.area / area

    def location2d_by_params(self, camera, area, center):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
        (in pixels)
        :param center: the center (x,y) of this object in the frame
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame_center = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_center = np.array(frame_center) / 2
        x, y = np.array(center) - frame_center
        alpha = x * camera.view_range / frame_center[0]
        return np.array([np.sin(alpha), np.cos(alpha)]) * self.distance_by_params(camera, area)

    def location3d(self, camera, pipeline, frame=None):
        """
        calculates the 2d location [x z] between the object and the camera
        :param camera: the camera, can be either Camera or CameraList
        :param pipeline: a pipeline that returns the contour of the object
        :param frame: optional, a frame to be used instead of the next image from the camera
        :return: a 3d vector of the relative [x y z] location between the object and the camera (in meters)
        """
        frame = camera.read() if frame is None else frame
        cnt = pipeline(frame)
        d_norm = self.distance_by_contours(camera, cnt)
        m = cv2.moments(cnt)
        frame_center = np.array(frame.shape[:2][::-1]) / 2
        vp = m['m10'] / (m['m00'] + 0.000001), m['m01'] / (m['m00'] + 0.000001)
        x, y = np.array(vp) - frame_center
        alpha = x * camera.view_range / frame_center[0]
        beta = y * camera.view_range / frame_center[1]
        return np.array([np.sin(alpha), np.sin(beta), np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]) * d_norm

    def location3d_by_contours(self, camera, cnt):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame_center = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_center = np.array(frame_center) / 2
        m = cv2.moments(cnt)
        vp = m['m10'] / (m['m00'] + 0.000001), m['m01'] / (m['m00'] + 0.000001)
        x, y = np.array(vp) - frame_center
        alpha = x * camera.view_range / frame_center[0]
        beta = y * camera.view_range / frame_center[1]
        return np.array([np.sin(alpha), np.sin(beta), np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]) \
               * self.distance_by_contours(camera, cnt)

    def location3d_by_params(self, camera, area, center):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
        (in pixels)
        :param center: the center (x,y) of this object in the frame
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame_center = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_center = np.array(frame_center) / 2
        x, y = np.array(center) - frame_center
        alpha = x * camera.data.view_range / frame_center[0]
        beta = y * camera.data.view_range / frame_center[1]
        return np.array([np.sin(alpha), np.sin(beta), np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]) \
               * self.distance_by_params(camera, area)
