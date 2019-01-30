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

NUMBER_OF_CAMERAS = 2


def main():
    algo_lock = Lock()
    current_algorithm = [lambda x, y: 0]

    cameras = CameraList(range(NUMBER_OF_CAMERAS), [LIFECAM_STUDIO, LIFECAM_3000])

    def change_algorithm(value):
        with algo_lock:
            current_algorithm[0] = ALGORITHMS_DICT[value]

    def change_camera(value):
        cameras.set_camera(int(value))

    conn = net_init()
    conn.add_entry_change_listener(change_algorithm, 'algorithm')
    conn.add_entry_change_listener(change_camera, 'camera')

    while True:
        try:
            sys.stdout.write(conn.get('algorithm', ""))
            with algo_lock:
                current_algorithm[0](cameras, conn)
        except VisionWarning as vw:
            print(vw, file=sys.stderr)
        except VisionException as ve:
            print(ve, file=sys.stderr)


if __name__ == '__main__':
    main()
