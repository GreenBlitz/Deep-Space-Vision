import numpy as np
import cv2
from tools.cameras import Camera, CameraList
from tools.pipeline import PipeLine


class ImageObject:
    def __init__(self, area, shape=None ,three_d_shape=None):
        """
        constructor of the image object
        which is an object on field
        :param area: the area of the object (in squared meters), float
        :param shape: optional, the shape of the object (2d)
        used to test if a recorded object is the object represented by the image object
        :param three_d_shape: the three dimensional shape of the object
        used to estimate things like the center of the actual object
        """
        self.area = area
        self.shape = shape
        self.three_d_shape = three_d_shape

    def distance(self, camera:Camera or CameraList, pipeline: PipeLine, frame=None) -> float:
        return camera.constant*self.area/pipeline(camera.read()[1] if frame is None else frame)

    def location2d(self, camera: Camera or CameraList, pipeline: PipeLine, frame:np.ndarray=None,
                   camera_height=0, camera_angle=0.0) -> np.ndarray:
        frame = camera.read() if frame is None else frame
        cnt = pipeline(frame)
        d_norm = self.distance(camera, pipeline + PipeLine(lambda f: np.sqrt(cv2.contourArea(cnt))))
        m = cv2.moments(cnt)
        frame_center = np.array(frame.shape[:2][::-1]) / 2
        vp = m['m10'] / (m['m00'] + 0.000001), m['m01'] / (m['m00'] + 0.000001)
        #if camera_height != 0:
        #    rotation = np.array([[np.cos(camera_angle), np.sin(camera_angle)],
        #                         [np.sin(-camera_angle), np.cos(camera_angle)]])
        #    vp = rotation.dot(np.array([vp]).T).reshape(2)
        x, y = np.array(vp) - frame_center
        alpha = x*camera.view_range/frame_center[0]
        return np.array([np.sin(alpha), np.cos(alpha)])*d_norm