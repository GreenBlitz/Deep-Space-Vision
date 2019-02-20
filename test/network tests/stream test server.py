import socket
import sys
import cv2
import pickle
import numpy as np
import struct  ## new
from utils.net import *

HOST = '0.0.0.0'
PORT = 8089


def main():
    server = StreamServer()
    while True:
        frame = server.get_frame()
        cv2.imshow('stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
