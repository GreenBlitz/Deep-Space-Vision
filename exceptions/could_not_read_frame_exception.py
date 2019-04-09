from .vision_exception import VisionException


class CouldNotReadFrameException(VisionException):
    def __init__(self, *args, **kwargs):
        VisionException.__init__(self, *args, **kwargs)
