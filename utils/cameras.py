from threading import Lock
from copy import deepcopy
import cv2
import numpy as np


class CameraData:
    def __init__(self, surface_constant, fov):
        self.constant = surface_constant
        self.view_range = fov

    def __cmp__(self, other):
        return self.constant == other.constant and self.view_range == other.view_range


class Camera:
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
        self.data = deepcopy(data)
        self.port = port
        self.capture = cv2.VideoCapture(port)

    def read(self):
        return self.capture.read()

    def get(self, item):
        return self.capture.get(item)

    def set(self, prop_id, value):
        return self.capture.set(prop_id, value)

    def release(self):
        return self.capture.release()

    def set_exposure(self, exposure):
        self.capture.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def toggle_auto_exposure(self, auto=0):
        self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto)

    def resize(self, x_factor, y_factor):
        assert x_factor > 0 and y_factor > 0
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) * x_factor)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT) * y_factor)
        self.data.constant *= np.sqrt(x_factor * y_factor)

    def set_frame_size(self, width, height):
        assert width > 0 and height > 0
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.data.constant = np.sqrt(width * height)

    @property
    def view_range(self): return self.data.view_range

    @property
    def constant(self): return self.data.constant


class CameraList:
    """
    behaves as both a camera and a list of cameras
    camera list holds in it a dictionary of cameras referenced as cameras
    and also a single camera to be the current camera used for every operation on the camera list
    as a single camera
    """

    def __init__(self, ports, cameras_data, select_cam=0):
        """
        :param ports: the ports of the cameras
        :param cameras_data: the camera data object describing each port
        :param select_cam: optional, an initial camera to be selected
        """
        self.cameras = {}
        self.camera = None
        for i, c in enumerate(set(ports)):
            self.cameras[c] = Camera(c, cameras_data[i])
        self.lock = Lock()
        self.camera = self.cameras[select_cam] if select_cam in self.cameras else None

    def __getitem__(self, item):
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

    def read(self, *args):
        if len(args) == 0:
            with self.lock:
                return self.camera.read()
        images = []
        with self.lock:
            for port in args:
                images.append(self.cameras[port].read())
        return images

    def add_new_camera(self, port, data):
        with self.lock:
            self.cameras[port] = Camera(port, data)

    def add_camera(self, cam):
        with self.lock:
            self.camera[cam.port] = cam

    def release(self):
        with self.lock:
            del self.cameras[self.camera.port]
            self.camera = None

    def __del__(self):
        with self.lock:
            for cap in self.cameras.values():
                cap.release()

    def default(self):
        with self.lock:
            self.camera = self.cameras[self.cameras.keys()[0]]

    def get(self, arg):
        with self.lock:
            return self.camera.get(arg)

    def read_all(self):
        with self.lock:
            return {port: self.cameras[port].read()[1] for port in self.cameras}

    def set(self, prop_id, value):
        with self.lock:
            return self.camera.set(prop_id, value)

    def set_exposure(self, exposure):
        with self.lock:
            self.camera.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def toggle_auto_exposure(self, auto=0):
        with self.lock:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto)

    @property
    def view_range(self):
        with self.lock:
            return self.camera.view_range

    @property
    def constant(self):
        with self.lock:
            return self.camera.constant

    @property
    def data(self):
        with self.lock:
            return self.camera.data

    def resize(self, x_factor, y_factor):
        assert x_factor > 0 and y_factor > 0
        with self.lock:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera.get(cv2.CAP_PROP_FRAME_WIDTH) * x_factor)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT) * y_factor)
            self.data.constant *= np.sqrt(x_factor * y_factor)

    def set_frame_size(self, width, height):
        assert width > 0 and height > 0
        with self.lock:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.data.constant = np.sqrt(width * height)
