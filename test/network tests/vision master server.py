from models import *
from utils import *
from utils.net import *


def main():
    conn = TableConn()
    server = StreamServer()
    while True:
        frame = server.get_frame()
        cv2.imshow('stream', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('0'):
            conn.set('camera', 0)
        if k == ord('1'):
            conn.set('camera', 1)


if __name__ == '__main__':
    main()
