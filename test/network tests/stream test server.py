from utils.net import *

HOST = '0.0.0.0'
PORT = 8089


def main():
    server = StreamServer()
    while True:
        frame = server.get_frame()
        cv2.imshow('stream', cv2.resize(frame, (0,0), fx=1.2/0.4, fy=1.2/0.4))
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
