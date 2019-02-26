from utils import *
from models import *
from utils.net import *


def main():
    camera = StreamCamera(0, LIFECAM_3000, StreamClient(ip='127.0.0.1', fx=1, fy=1))
    print(camera.im_height)
    print(camera.im_width)
    camera.toggle_stream(True)
    camera.resize(0.4, 0.4)
    while True:
        ok, frame = camera.read()


if __name__ == '__main__':
    main()
