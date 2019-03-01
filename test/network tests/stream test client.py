from utils import *
from models import *
from utils.net import *


def main():
    camera = StreamCamera(0, LIFECAM_3000,
                          StreamClient(ip='10.45.90.60', port=5801, fx=0.5, fy=0.5, max_fps=24, use_grayscale=False))
    print(camera.im_height)
    print(camera.im_width)
    camera.toggle_stream(True)
    camera.resize(0.4, 0.4)
    while True:
        ok, frame = camera.read()


if __name__ == '__main__':
    main()
