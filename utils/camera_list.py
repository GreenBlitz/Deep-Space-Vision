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
        self.cameras = cameras[:]
        self.camera = self.cameras[select_cam] if select_cam is not None else None

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
            return [cam.read() for cam in self.cameras]
        return self.camera.read()

    def add_camera(self, cam):
        self.camera.append(cam)

    def release(self, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.release()
        else:
            self.camera.release()
            self.camera = None

    def default(self):
        self.camera = self.cameras[list(self.cameras)[0]]

    def get(self, arg, foreach=False):
        if foreach:
            return [cam.get(arg) for cam in self.cameras]
        return self.camera.get(arg)

    def set(self, prop_id, value, foreach=False):
        if foreach:
            return [cam.set(prop_id, value) for cam in self.cameras]
        return self.camera.set(prop_id, value)

    def set_exposure(self, exposure, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_exposure(exposure)
        else:
            return self.camera.set_exposure(exposure)

    def toggle_auto_exposure(self, auto, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.toggle_auto_exposure(auto)
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
            for cam in self.cameras:
                cam.resize(x_factor, y_factor)
        else:
            self.camera.resize(x_factor, y_factor)

    def rescale(self, factor, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.rescale(factor)
        else:
            self.camera.resize(factor)

    def set_frame_size(self, width, height, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_frame_size(width, height)
        else:
            self.camera.set_frame_size(width, height)

    def toggle_stream(self, should_stream, foreach=False):
        if foreach:
            for cam in self.cameras:
                if isinstance(cam, StreamCamera):
                    cam.toggle_stream(should_stream)
        else:
            if isinstance(self.camera, StreamCamera):
                self.camera.toggle_stream(should_stream)

    @property
    def width(self):
        return self.get(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def height(self):
        return self.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def rotate(self, cv_angle, foreach=False):
        if foreach:
            for i in self.cameras:
                self.cameras[i].rotate(cv_angle)
        else:
            self.camera.rotate(cv_angle)
