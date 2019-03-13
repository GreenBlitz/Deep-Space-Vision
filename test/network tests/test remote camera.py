from utils.net import *
from utils import *

HOST = '0.0.0.0'
PORT = 8089


def main():
    server = TCPStreamServer(ip='0.0.0.0', port=5802, fx=1, fy=1)
    camera = RemoteCamera(cam_index=0, stream_server=server, network_table_ip='10.45.90.2')
    camera.toggle_stream(True)
    camera.set_frame_size(100, 100)
    while True:
        ok, frame = camera.read()
        cv2.imshow('stream', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break
        if k == ord('e'):
            print('resize server')
            camera.set_exposure(-12)
        if k == ord('r'):
            print('resize server')
            camera.set_exposure(-5)


if __name__ == '__main__':
    main()
