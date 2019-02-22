from models import *
from utils.net import *
from utils import *
from main import *

FRONT_LEFT_CAM_PORT = 0
FRONT_RIGHT_CAM_PORT = 1
BACK_CAM_PORT = 2


def main():
    print("starting vision master")
    print("initializing connection to stream server")
    stream_ports = [1]
    stream_client_main = StreamClient()
    cameras = CameraList([
        StreamCamera(FRONT_LEFT_CAM_PORT, LIFECAM_3000, stream_client_main),
        StreamCamera(FRONT_RIGHT_CAM_PORT, LIFECAM_3000, stream_client_main),
        Camera(BACK_CAM_PORT, LIFECAM_3000)
    ])

    conn = net_init()

    def camera_change_callback(cam):
        if cameras.port == cam:
            return
        if cam == BACK_CAM_PORT:
            cameras.set_camera(BACK_CAM_PORT)
            return
        cameras.set_camera(cam)
        stream_ports[0] = FRONT_LEFT_CAM_PORT if cam == FRONT_RIGHT_CAM_PORT else FRONT_RIGHT_CAM_PORT
        cameras[stream_ports[0]].toggle_auto_exposure(0.75)
        cameras.toggle_auto_exposure(0.25)

    conn.add_entry_change_listener(camera_change_callback, 'camera')
    conn.add_entry_change_listener(lambda should_stream: cameras.toggle_stream(should_stream, foreach=True), 'stream')
    conn.add_entry_change_listener(lambda should_stream: cameras[0].toggle_stream(should_stream), 'stream_cam_front')
    conn.add_entry_change_listener(lambda should_stream: cameras[1].toggle_stream(should_stream), 'stream_cam_back')

    print("setting camera auto exposure to false")

    cameras.toggle_stream(True, foreach=True)

    conn.set('algorithm', 'send_location')
    prev_algo = None
    while True:
        print('iterating...')
        algo = conn.get('algorithm')
        cameras[stream_ports[0]].read()
        if algo == 'send_cargo':
            if algo != prev_algo:
                init_send_cargo(cameras, conn)
            send_cargo(cameras, conn)

        if algo == 'send_hatch':
            if algo != prev_algo:
                init_send_hatch(cameras, conn, cameras[stream_ports[0]])
            send_hatch(cameras, conn)

        if algo == 'send_location':
            if algo != prev_algo:
                init_send_location(cameras, conn, cameras[stream_ports[0]])
            send_location(cameras, conn)

        if algo == 'send_hatch_panel':
            if algo != prev_algo:
                init_send_hatch_panel(cameras, conn)
            send_hatch_panel(cameras, conn)

        prev_algo = algo


if __name__ == '__main__':
    main()
