import cv2
import numpy as np
from threading import Lock

class Camera(cv2.VideoCapture):
    def __init__(self, index, const):
        cv2.VideoCapture.__init__(self, index)
        self.constant = float(const)
        self.index = index
    def __del__(self):
        self.release()


class CameraList:
    def __init__(self, cams, constants, select_cam=0):
        self.cameras = []
        self.camera = None
        for i, c in enumerate(set(cams)):
            self.cameras.append(Camera(c, constants[i]))
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
            for i in set(args):
                images.append(self.cameras[i].read())
            return images

    def add_camera(self, index:int or str, constant: float or int):
        with self.lock:
            self.cameras.append(Camera(index, constant))
            self.sort()

    def sort(self):
        with self.lock:
            self.cameras.sort(key=lambda x: x.index)

    def set_camera_by_index(self, index:int or str):
        with self.lock:
            for i in self.cameras:
                if i.index == index:
                    self.camera = i
                    return