from .net_consts import *
from exceptions import *
import socket
import pickle
import struct
import cv2

MAX_UDP_MESSAGE_LENGTH = 40000


class StreamServer:
    def __init__(self, ip='0.0.0.0', port=STREAM_PORT, fx=1, fy=1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((ip, port))
        # self.socket.listen(10)
        # self.socket, addr = self.socket.accept()
        self.payload_size = struct.calcsize("I")
        self.data = b''
        self.fx = fx
        self.fy = fy

    def get_frame(self):
        while len(self.data) < self.payload_size:
            self.data += self.socket.recv(2**20)

        packed_msg_size = self.data[:self.payload_size]

        self.data = self.data[self.payload_size:]

        msg_size = struct.unpack("I", packed_msg_size)[0]

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)
        if frame is None:
            return None
        frame = cv2.imdecode(frame, -1)
        return cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
