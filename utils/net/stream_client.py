import socket
from .net_consts import *
import cv2
import pickle
import struct
import numpy as np

MAX_UDP_MESSAGE_LENGTH = 40000


class StreamClient:
    def __init__(self, ip=STREAM_IP, port=STREAM_PORT, im_encode='.jpg', use_grayscale=False, fx=1, fy=1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (ip, port)
        # self.socket.connect(self.server_addr)
        self.im_encode = im_encode
        self.use_grayscale = use_grayscale
        self.payload_size = struct.calcsize("I")
        self.fx = fx
        self.fy = fy

    def send_frame(self, frame):

        if frame is not None:
            frame = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
            if self.use_grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.imencode(self.im_encode, frame)[1]
        data = pickle.dumps(frame)
        data = struct.pack("I", len(data)) + data
        self.socket.sendto(data, self.server_addr)
