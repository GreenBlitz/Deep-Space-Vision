from .stream_camera import *
from threading import Lock


class CameraList:
    """
    behaves as both a camera and a list of cameras
    camera list holds in it a dictionary of cameras referenced as cameras
    and also a single camera to be the current camera used for every operation on the camera list
    as a single camera
    """

    def __init__(self, cameras, select_cam=0):
        """
        :param cameras: list of the cameras which will be part of the camera list
        you can also add and remove cameras later using the
        :param select_cam: optional, an initial camera to be selected
        """
        self.cameras = {}
        for i in cameras:
            self.cameras[i.port] = i
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

    def set_exposure(self, exposure, foreach=False):
        if foreach:
            with self.lock:
                for i in self.cameras:
                    self.cameras[i].set_exposure(exposure)
        else:
            with self.lock:
                return self.camera.set_exposure(exposure)

    def toggle_auto_exposure(self, auto, foreach=False):
        if foreach:
            for i in self.cameras:
                self.cameras[i].toggle_auto_exposure(auto)
        else:
            with self.lock:
                return self.camera.toggle_auto_exposure(auto)

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

    @property
    def port(self):
        with self.lock:
            return self.camera.port

    def resize(self, x_factor, y_factor, foreach=False):
        if foreach:
            with self.lock:
                for i in self.cameras:
                    self.cameras[i].resize(x_factor, y_factor)
        else:
            with self.lock:
                self.camera.resize(x_factor, y_factor)

    def set_frame_size(self, width, height, foreach=False):
        if foreach:
            with self.lock:
                for i in self.cameras:
                    self.cameras[i].set_frame_size(width, height)
        else:
            with self.lock:
                self.camera.set_frame_size(width, height)

    def toggle_stream(self, should_stream, foreach=False):
        if foreach:
            for i in self.cameras:
                if isinstance(self.cameras[i], StreamCamera):
                    self.cameras[i].toggle_stream(should_stream)
        else:
            if isinstance(self.camera, StreamCamera):
                with self.lock:
                    self.camera.toggle_stream(should_stream)

    @property
    def width(self):
        return self.get(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def height(self):
        return self.get(cv2.CAP_PROP_FRAME_HEIGHT)
