from models import *
from utils.net import *
from utils import *
from main import *


def main():
    print("starting vision master")
    cameras = CameraList([

    ])

    cameras.resize(0.5, 0.5)
    
    conn = net_init()

    conn.add_entry_change_listener(lambda cam: cameras.set_camera(int(cam)), 'camera')
    conn.add_entry_change_listener('camera')
     
    print("setting camera exposure")
    cameras.toggle_auto_exposure(0.25)
    cameras.set_exposure(1)

    conn.set('algorithm', 'send_cargo')

    while True:
        algo = conn.get('algorithm')
        if algo == 'send_cargo':
            send_cargo(cameras, conn)
        if algo == 'send_hatch':
            send_hatch(cameras, conn)


if __name__ == '__main__':
    main()
