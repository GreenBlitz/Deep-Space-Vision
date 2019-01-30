from models import *
from utils.net import *
from utils import *
from exceptions import *
import sys
from threading import Lock
from main import *

ALGORITHMS_DICT = {
    'send_cargo': send_cargo,
    'send_hatch': send_hatch

}

NUMBER_OF_CAMERAS = 1


def main():
    algo_lock = Lock()
    current_algorithm = [lambda x, y: 0]

    cameras = CameraList(range(NUMBER_OF_CAMERAS), [LIFECAM_STUDIO])
    print('hello')
    def change_algorithm(value):
        print('changing algorithm to: %s' % value)
        current_algorithm[0] = ALGORITHMS_DICT[value]

    def change_camera(value):
        cameras.set_camera(int(value))
    
    cameras.camera.resize(0.25, 0.25)
    change_algorithm('send_cargo')
    conn = net_init()
    conn.add_entry_change_listener(change_algorithm, 'algorithm')
    conn.add_entry_change_listener(change_camera, 'camera')
    #import os
    #os.system('v4l2-ctl -d /dev/video0 -c exposure_auto=1')
    #os.system('v4l2-ctl -d /dev/video0 -c exposure_absolute=6')
    while True:
        try:
            current_algorithm[0](cameras.camera, conn)
        except VisionWarning as vw:
            print(vw, file=sys.stderr)
        except VisionException as ve:
            print(ve, file=sys.stderr)


if __name__ == '__main__':
    main()
