from utils import *
from models import *
from utils.net import *


def main():
    camera = BroadcastCamera(0, LIFECAM_3000, StreamClient(ip='127.0.0.1', port=5802), cam_index=0,
                             network_table_ip='10.45.90.2')
    print(camera.im_height)
    print(camera.im_width)
    while True:
        try:
            ok, frame = camera.read()
        except:
            print(camera.width)
            print(camera.height)


if __name__ == '__main__':
    main()
