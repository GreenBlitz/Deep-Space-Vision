from threading import Lock
import cv2


class CameraData:
    def __init__(self, surface_constant, fov):
        self.constant = surface_constant
        self.view_range = fov


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
        self.constant = float(data.constant)
        self.data = data
        self.view_range = data.view_range
        self.capture = cv2.VideoCapture(port)

    def __getattr__(self, attr):
        return self.capture.__getattribute__(attr)  # this fucking works karel


class CameraList:
    """
    behaves as both a camera and a list of cameras
    camera list holds in it a dictionary of cameras referenced as cameras
    and also a single camera to be the current camera used for every operation on the camera list
    as a single camera
    """

    def __init__(self, cams, cameradata, select_cam=0):
        """
        :param cams: the ports of the cameras
        :param cameradata: the camera data object describing each port
        :param select_cam: optional, an initial camera to be selected
        """
        self.cameras = {}
        self.camera = None
        for i, c in enumerate(set(cams)):
            self.cameras[c] = (Camera(c, cameradata[i]))
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
        with self.lock:
            if len(args) == 0:
                return self.camera.read()
            images = []
            for i in args:
                images.append(self.cameras[i].read())
            return images

    def add_camera(self, index, data):
        with self.lock:
            self.cameras[index] = Camera(index, data)

    def __getattr__(self, item):
        return self.camera.__getattribute__(item)

    def release(self):
        with self.lock:
            del self.cameras[self.camera.index]
            self.camera = None

    def default(self):
        with self.lock:
            self.camera = self.cameras[list(self.cameras)[0]]

    def get(self, arg):
        with self.lock:
            return self.camera.get(arg)
