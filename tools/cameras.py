import cv2
import numpy as np
from threading import Lock

class Camera(cv2.VideoCapture):
    def __init__(self, index, const, angle):
        cv2.VideoCapture.__init__(self, index)
        self.constant = float(const)
        self.index = index
        self.view_range = angle
    def __del__(self):
        self.release()


class CameraList:
    def __init__(self, cams, constants, select_cam=0):
        self.cameras = {}
        self.camera = None
        for i, c in enumerate(set(cams)):
            self.cameras[c] = (Camera(c, constants[i]))
        self.lock = Lock()
        self.camera = self.cameras[select_cam]

    def __getitem__(self, item:int) -> cv2.VideoCapture:
        with self.lock:
            return self.cameras[item]

    def set_camera(self, index):
        with self.lock:
            self.camera = self.cameras[index]

    def __delitem__(self, key):
        with self.lock:
            if self.camera is self.cameras[key]:
                self.camera = None
            del self.cameras[key]

    def read(self, *args) -> np.ndarray or list:
        with self.lock:
            if len(args) == 0:
                return self.camera.read()
            images = []
            for i in args:
                images.append(self.cameras[i].read())
            return images

    def add_camera(self, index:int or str, constant: float or int):
        with self.lock:
            self.cameras[index] = Camera(index, constant)
            self.sort()

    @property
    def constant(self):
        with self.lock:
            return self.camera.constant

    @property
    def index(self):
        with self.lock:
            return self.camera.index

    @property
    def view_range(self):
        with self.lock:
            return self.camera.view_range

    def release(self):
        with self.lock:
            del self.cameras[self.camera.index]
            self.camera = None

    def default(self):
        with self.lock:
            self.camera = self.cameras[list(self.cameras)[0]]
