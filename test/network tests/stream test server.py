from utils.net import *

HOST = '0.0.0.0'
PORT = 8089


def main():
    server1 = StreamServer(port=8089)
    server2 = StreamServer(port=8090)
    while True:
        frame1 = server1.get_frame()
        frame2 = server2.get_frame()
        cv2.imshow('stream1', frame1)
        cv2.imshow('stream2', frame2)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
