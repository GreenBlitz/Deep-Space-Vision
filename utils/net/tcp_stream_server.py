from .net_consts import *
from exceptions import *
import socket
import pickle
import struct
import cv2
import time


class TCPStreamServer:
    def __init__(self, ip='0.0.0.0', port=STREAM_PORT, fx=1, fy=1, im_encode='.jpg', use_grayscale=False, max_fps=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.socket.bind(self.server_addr)
        self.socket.listen(10)
        self.socket, addr = self.socket.accept()
        self.payload_size = struct.calcsize("I")
        self.use_grayscale = use_grayscale
        self.im_encode = im_encode
        self.fx = fx
        self.fy = fy
        self.max_fps = max_fps
        self.prev_time = 0

    def send_frame(self, frame):
        if self.max_fps is not None and (time.time() - self.prev_time)*self.max_fps < 1:
            return
        if frame is not None:
            frame = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
            if self.use_grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.imencode(self.im_encode, frame)[1]
        data = pickle.dumps(frame)
        data = struct.pack("I", len(data)) + data
        self.socket.send(data)  # to(data, self.server_addr)
        self.prev_time = time.time()
