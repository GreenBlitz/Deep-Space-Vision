from utils.net import *
from utils import *
from main import *

FRONT_LEFT_CAM_PORT = 0
FRONT_RIGHT_CAM_PORT = 1


def cam_change_callback(cam, cameras):
    if cam != cameras.port:
        cameras.set_camera(cam)


def main():
    print("starting vision master")
    print("initializing connection to stream server")
    stream_client_main = StreamClient(ip='10.45.90.193', port=5801, fx=0.4, fy=0.4, use_grayscale=True, max_fps=20)
    cameras = CameraList([
        StreamCamera(FRONT_LEFT_CAM_PORT, LIFECAM_3000, stream_client_main, should_stream=True)
        # StreamCamera(FRONT_RIGHT_CAM_PORT, LIFECAM_3000, stream_client_main, should_stream=True)
    ])

    conn = TableConn(ip='10.45.90.2')

    # conn.add_entry_change_listener(lambda cam: cam_change_callback(int(cam), cameras), 'camera')
    # conn.add_entry_change_listener(lambda should_stream: cameras[0].toggle_stream(should_stream), 'stream_cam_front')
    # conn.add_entry_change_listener(lambda should_stream: cameras[1].toggle_stream(should_stream), 'stream_cam_back')

    print("setting camera auto exposure to false")

    conn.set('algorithm', 'send_hatch')
    prev_algo = None
    while True:
        algo = conn.get('algorithm')
        print("algorithm: %s" % algo)
        if algo == 'send_cargo':
            if algo != prev_algo:
                init_send_cargo(cameras, conn)
            send_cargo(cameras, conn)

        if algo == 'send_hatch':
            if algo != prev_algo:
                init_send_hatch(cameras, conn)
            send_hatch(cameras, conn)

        if algo == 'send_location':
            if algo != prev_algo:
                init_send_location(cameras, conn)
            send_location(cameras, conn)

        if algo == 'send_hatch_panel':
            if algo != prev_algo:
                init_send_hatch_panel(cameras, conn)
            send_hatch_panel(cameras, conn)

        if algo == 'send_stream':
            if algo != prev_algo:
                init_send_stream(cameras, conn)
            send_stream(cameras, conn)

        prev_algo = algo


if __name__ == '__main__':
    main()
