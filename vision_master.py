from models import *
from utils.net import *
from utils import *
from exceptions import *
import sys
import threading
from main import *
import os

ALGORITHMS_DICT = {
    'send_cargo': send_cargo,
    'send_hatch': send_hatch,
    'send_fuel': send_fuel,
    'send_trash': send_trash
}

NUMBER_OF_CAMERAS = 1


class VisionMaster:
    def __init__(self, algorithm, camera, conn):
        self.__current = algorithm
        self.__lock = threading.RLock()
        self.__camera = camera
        self.__conn = conn

    def apply(self):
        with self.__lock:
            self.__current(self.__camera, self.__conn)

    def __call__(self):
        self.apply()

    def get_current_algorithm(self):
        with self.__lock:
            return self.__current

    def set_current_algorithm(self, value):
        with self.__lock:    
            print('changing algorithm to: %s' % value)
            self.__current = value

    def get_current_camera(self):
        with self.__lock:
            return self.__camera

    def set_current_camera(self, value):
        with self.__lock:
            self.__camera = value


def main():
    print("starting vision master")
    cameras = CameraList(range(NUMBER_OF_CAMERAS), [LIFECAM_STUDIO])
    cameras.camera.resize(0.5, 0.5)
    
    conn = net_init()

    print("creating vision master")
    master = VisionMaster(ALGORITHMS_DICT['send_cargo'], cameras.camera, conn)
   
    print("registering connection listeners")
    conn.add_entry_change_listener(lambda algo: master.set_current_algorithm(ALGORITHMS_DICT[algo]), 'algorithm')
    conn.add_entry_change_listener(lambda cam: master.set_current_camera(cameras[int(cam)]), 'camera')
     
    print("setting camera exposure")
    os.system('v4l2-ctl -d /dev/video0 -c exposure_auto=1')
    # os.system('v4l2-ctl -d /dev/video0 -c exposure_absolute=6')
    cameras.set_exposure(-6)

    while True:
        try:
            master.apply()
        except VisionWarning as vw:
            print(vw, file=sys.stderr)
        except VisionException as ve:
            print(ve, file=sys.stderr)


if __name__ == '__main__':
    main()
