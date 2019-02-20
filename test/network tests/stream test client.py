from utils import *
from models import *
import socket
import pickle
import struct
from utils.net import *


def main():
    camera = StreamCamera(PORT, LIFECAM_3000, StreamClient(ip='192.168.1.39'))
    camera.toggle_stream(True)
    camera.set_frame_size(100, 100)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
