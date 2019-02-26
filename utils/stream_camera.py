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
        self.im_width = cv2.VideoCapture.get(self, cv2.CAP_PROP_FRAME_WIDTH)
        self.im_height = cv2.VideoCapture.get(self, cv2.CAP_PROP_FRAME_HEIGHT)

    def read(self, image=None):
        ok, frame = Camera.read(self, image)
        if not ok:
            return ok, frame
        if self.should_stream and ok:
            self.stream_client.send_frame(frame)
        return ok, cv2.resize(frame, (int(self.im_width), int(self.im_height)))

    def toggle_stream(self, should_stream=False):
        self.should_stream = should_stream

    def get(self, propId):
        if propId == cv2.CAP_PROP_FRAME_WIDTH:
            return self.im_width
        elif propId == cv2.CAP_PROP_FRAME_HEIGHT:
            return self.im_height
        return Camera.get(self, propId)

    def resize(self, x_factor, y_factor):
        self.im_width = self.im_width * x_factor
        self.im_height = self.im_height * y_factor
        self.data.constant *= np.sqrt(x_factor*y_factor)

    def set_frame_size(self, width, height):
        self.im_width = width
        self.im_height = height
        self.data.constant = np.sqrt(width * height)
