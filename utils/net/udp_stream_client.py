import socket
from .net_consts import *
import cv2
import pickle
import struct
import time


class UDPStreamClient:
    def __init__(self, ip=STREAM_IP, port=STREAM_PORT, fx=1, fy=1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.socket.bind(self.server_addr)
        self.payload_size = struct.calcsize("I")
        self.fx = fx
        self.fy = fy
        self.data = b''

    def get_frame(self):
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