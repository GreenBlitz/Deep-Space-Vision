from .stream_camera import *


class CameraList:
    """
    behaves as both a camera and a list of cameras
    camera list holds in it a dictionary of cameras referenced as cameras
    and also a single camera to be the current camera used for every operation on the camera list
    as a single camera
    """

    def __init__(self, cameras, select_cam=None):
        """
        :param cameras: list of the cameras which will be part of the camera list
        you can also add and remove cameras later using the
        :param select_cam: optional, an initial camera to be selected
        """
        self.cameras = {}
        if select_cam is None and len(cameras) > 0:
            select_cam = cameras[0].port
        for i in cameras:
            self.cameras[i.port] = i
        self.camera = self.cameras[select_cam] if select_cam in self.cameras else None

    def __getitem__(self, item):
        return self.cameras[item]

    def set_camera(self, index):
        self.camera = self.cameras[index]

    def __delitem__(self, key):
        if self.camera is self.cameras[key]:
            self.camera = None
        del self.cameras[key]

    def read(self, foreach=False):
        if foreach:
            return {port: self[port].read()[1] for port in self.cameras}
        return self.camera.read()

    def add_camera(self, cam):
        self.camera[cam.port] = cam

    def release(self):
        del self.cameras[self.camera.port]
        self.camera = None

    def __del__(self):
        for cap in self.cameras.values():
            cap.release()

    def default(self):
        self.camera = self.cameras[list(self.cameras.keys())[0]]

    def get(self, arg, foreach=False):
        if foreach:
            return {port: self[port].get(arg) for port in self.cameras}
        return self.camera.get(arg)

    def set(self, prop_id, value, foreach=False):
        if foreach:
            return {port: self[port].set(prop_id, value) for port in self.cameras}
        return self.camera.set(prop_id, value)

    def set_exposure(self, exposure, foreach=False):
        if foreach:
            for i in self.cameras:
                self.cameras[i].set_exposure(exposure)
        else:
            return self.camera.set_exposure(exposure)

    def toggle_auto_exposure(self, auto, foreach=False):
        if foreach:
            for i in self.cameras:
                self.cameras[i].toggle_auto_exposure(auto)
        else:
            return self.camera.toggle_auto_exposure(auto)

    @property
    def view_range(self):
        return self.camera.view_range

    @property
    def constant(self):
        return self.camera.constant

    @property
    def data(self):
        return self.camera.data

    @property
    def port(self):
        return self.camera.port

    def resize(self, x_factor, y_factor, foreach=False):
        if foreach:
            for i in self.cameras:
                self.cameras[i].resize(x_factor, y_factor)
        else:
            self.camera.resize(x_factor, y_factor)

    def set_frame_size(self, width, height, foreach=False):
        if foreach:
            for i in self.cameras:
                self.cameras[i].set_frame_size(width, height)
        else:
            self.camera.set_frame_size(width, height)

    def toggle_stream(self, should_stream, foreach=False):
        if foreach:
            for i in self.cameras:
                if isinstance(self.cameras[i], StreamCamera):
                    self.cameras[i].toggle_stream(should_stream)
        else:
            if isinstance(self.camera, StreamCamera):
                self.camera.toggle_stream(should_stream)

    @property
    def width(self):
        return self.get(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def height(self):
        return self.get(cv2.CAP_PROP_FRAME_HEIGHT)
