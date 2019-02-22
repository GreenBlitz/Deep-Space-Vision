from .net_consts import *
import socket
import pickle
import struct
import cv2


class StreamServer:
    def __init__(self, ip='0.0.0.0', port=STREAM_PORT, fx=3, fy=3):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(10)
        self.socket, addr = self.socket.accept()
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

        while len(self.data) < msg_size:
            self.data += self.socket.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        frame = cv2.imdecode(pickle.loads(frame_data), -1)
        return cv2.resize(frame, (0,0), fx=self.fx, fy=self.fy)
