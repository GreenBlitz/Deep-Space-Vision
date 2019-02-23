from utils.net import *

HOST = '0.0.0.0'
PORT = 8089


def main():
    server1 = StreamServer(ip='0.0.0.0', port=5801)
    while True:
        frame1 = server1.get_frame()
        cv2.imshow('stream1', frame1)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
