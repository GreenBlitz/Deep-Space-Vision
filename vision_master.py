from utils.net import *
from utils import *
from main import *
from electronics import *

FRONT_LEFT_CAM_PORT = 0
FRONT_RIGHT_CAM_PORT = 1


def cam_change_callback(cam, cameras):
    if cam != cameras.port:
        cameras.set_camera(cam)


def main():
    print("starting vision master")
    print("initializing connection to stream server")
    stream_server_main = StreamServer(ip='0.0.0.0', port=5801, fx=0.3, fy=0.3, max_fps=24, use_grayscale=False)
    cameras = CameraList([
        StreamCamera(FRONT_LEFT_CAM_PORT, LIFECAM_3000, stream_server_main, should_stream=True)
    ])

    leds = LedRing(port=17)

    conn = TableConn(ip='10.45.90.2')

    # conn.add_entry_change_listener(lambda cam: cam_change_callback(int(cam), cameras), 'camera')
    # conn.add_entry_change_listener(lambda should_stream: cameras[0].toggle_stream(should_stream), 'stream_cam_front')
    # conn.add_entry_change_listener(lambda should_stream: cameras[1].toggle_stream(should_stream), 'stream_cam_back')

    cameras.resize(0.4, 0.4)

    print("setting camera auto exposure to true")

    conn.set('algorithm', 'send_stream')
    prev_algo = None
    while True:
        print('iterating...')
        algo = conn.get('algorithm')
        print(algo)
        if algo == 'send_cargo':
            if algo != prev_algo:
                init_send_cargo(cameras, conn, leds)
            send_cargo(cameras, conn)

        if algo == 'send_hatch':
            if algo != prev_algo:
                init_send_hatch(cameras, conn, leds)
            send_hatch(cameras, conn)

        if algo == 'send_location':
            if algo != prev_algo:
                init_send_location(cameras, conn, leds)
            send_location(cameras, conn)

        if algo == 'send_hatch_panel':
            if algo != prev_algo:
                init_send_hatch_panel(cameras, conn, leds)
            send_hatch_panel(cameras, conn)

        if algo == 'send_stream':
            if algo != prev_algo:
                init_send_stream(cameras, conn, leds)
            send_stream(cameras, conn)

        prev_algo = algo


if __name__ == '__main__':
    main()
