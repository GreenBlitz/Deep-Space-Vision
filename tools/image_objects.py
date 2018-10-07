import numpy as np
import cv2
from tools.cameras import Camera, CameraList


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

    def distance(self, camera:Camera or CameraList, pipeline) -> float:
        pass