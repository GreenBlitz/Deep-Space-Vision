from copy import deepcopy
import cv2
import numpy as np


class Camera(cv2.VideoCapture):
    """
    camera api used to measure distances and estimate locations by other functions
    """

    def __init__(self, port, data):
        """
        :param data: containing some required camera information, such as const and angle
        const: the camera constant, computed as the square root of the area in pixels of a 1x1 m board
        viewed from a distance of 1 meters, used to calculate distances by the formula: d = F*sqrt(S/P) where F is
        the camera constant, S is the area of the object in m^2 and P is the area in pixels
        angle: the viewing range of the camera, computed as the arctan of half of the maximum height of an object seen
        from a distance of 1m, used to find the [x z] location of objects
        :param port: the port of the camera
        """
        cv2.VideoCapture.__init__(self, port)
        self.data = deepcopy(data)
        self.port = port
        self.rotation_angle = None

    def set_exposure(self, exposure):
        return self.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def toggle_auto_exposure(self, auto):
        return self.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto)

    def resize(self, x_factor, y_factor):
        self.set(cv2.CAP_PROP_FRAME_WIDTH, self.get(cv2.CAP_PROP_FRAME_WIDTH) * x_factor)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, self.get(cv2.CAP_PROP_FRAME_HEIGHT) * y_factor)
        self.data.constant *= np.sqrt(x_factor * y_factor)

    def rescale(self, factor):
        self.set(cv2.CAP_PROP_FRAME_WIDTH, self.get(cv2.CAP_PROP_FRAME_WIDTH) * factor)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, self.get(cv2.CAP_PROP_FRAME_HEIGHT) * factor)
        self.data.constant *= factor

    def set_frame_size(self, width, height):
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.data.constant = np.sqrt(width * height)

    def read(self, image=None):
        ok, frame = cv2.VideoCapture.read(self)
        if self.rotation_angle is not None:
            frame = cv2.rotate(frame, self.rotation_angle)
        return ok, frame

    def rotate(self, cv_angle):
        self.rotation_angle = cv_angle

    @property
    def view_range(self): return self.data.view_range

    @property
    def constant(self): return self.data.constant

    @property
    def width(self): return self.get(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def height(self): return self.get(cv2.CAP_PROP_FRAME_HEIGHT)

