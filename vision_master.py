from models import *
from utils.net import *
from utils import *
from main import *

FRONT_CAM_STREAM_PORT = 8089
BACK_CAM_STREAM_PORT = 8090


def main():
    print("starting vision master")
    cameras = CameraList([
        StreamCamera(0, LIFECAM_3000, StreamClient(port=FRONT_CAM_STREAM_PORT), should_stream=True),
        StreamCamera(1, LIFECAM_3000, StreamClient(port=BACK_CAM_STREAM_PORT), should_stream=True)
    ])

    cameras.resize(0.5, 0.5)

    conn = net_init()

    conn.add_entry_change_listener(lambda cam: cameras.set_camera(int(cam)), 'camera')
    conn.add_entry_change_listener(lambda should_stream: cameras.toggle_stream(should_stream, foreach=True), 'stream')

    print("setting camera auto exposure to false")
    cameras.toggle_auto_exposure(0.25, foreach=True)

    conn.set('algorithm', 'send_cargo')
    prev_algo = conn.get('algorithm')
    while True:
        algo = conn.get('algorithm')
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


if __name__ == '__main__':
    main()
