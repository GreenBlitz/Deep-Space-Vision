import socket
from .net_consts import *
import cv2
import pickle
import struct


class StreamClient:
    def __init__(self, ip=STREAM_IP, port=STREAM_PORT, im_encode='.jpg'):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.socket.connect(self.server_addr)
        self.im_encode = im_encode

    def send_frame(self, frame):
        frame = cv2.imencode(self.im_encode, frame)[1]
        data = pickle.dumps(frame)
        self.socket.send(struct.pack("I", len(data)) + data)