import cv2
import numpy as np
from threading import Lock

class Camera:
    def __init__(self, index, const):
        self.init = cv2.VideoCapture(index)
        if not self.init.isOpened():
            raise Exception('could not connect to camera')
        self.constant = const
        self.lock = Lock()
    def __del__(self):
        with self.lock:
            self.init.release()
    def __call__(self, *args, **kwargs) -> np.ndarray:
        with self.lock:
            ok, frame = self.init.read()
            return frame


class CameraList:
    def __init__(self, cams, constants):
        self.cameras = []
        self.camera = None
        for i, c in enumerate(cams):
            self.cameras.append(Camera(c, constants[i]))
        self.lock = Lock()
    def __getitem__(self, item:int) -> cv2.VideoCapture:
        with self.lock:
            return self.cameras[item]
    def set_camera(self, index):
        with self.lock:
            self.camera = index
    def __delitem__(self, key):
        del self.cameras[key]
