from utils import *
from models import *
import socket
import pickle
import struct
from utils.net import *


def main():
    camera = StreamCamera(PORT, LIFECAM_3000, StreamClient(ip='192.168.1.39'))
    camera.toggle_stream(True)
    camera.set_frame_size(0.4, 0.4)
    while True:
        ok, frame = camera.read()


if __name__ == '__main__':
    main()
