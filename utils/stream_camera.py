from .camera import *


class StreamCamera(Camera):
    """
    a camera with an option to stream the image it reads
    """
    def __init__(self, port, data, stream_client, should_stream=False):
        """

        :param port: the camera port (see Camera constructor)
        :param data: the camera descriptor (see Camera constructor)
        :param stream_client: a StreamClient object used to stream the image
        :param should_stream:
        """
        Camera.__init__(self, port, data)
        self.stream_client = stream_client
        self.should_stream = should_stream
        self.im_width = self.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.im_height = self.get(cv2.CAP_PROP_FRAME_WIDTH)

    def read(self, image=None):
        ok, frame = Camera.read(self, image)
        if self.should_stream and ok:
            self.stream_client.send_frame(frame)
        return ok, frame

    def toggle_stream(self, should_stream=False):
        self.should_stream = should_stream
