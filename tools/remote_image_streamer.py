from models import *
from utils import *
from utils.net import *


def main():
    client = StreamClient(ip='10.45.90.193', port=5801, use_grayscale=False, fx=0.5, fy=0.5, max_fps=20)
    camera = StreamCamera(PORT, CameraData(0, 0), client, should_stream=True)
    camera.toggle_auto_exposure(0.25)
    camera.set_exposure(0)
    # camera.resize(0.4, 0.4)

    while True:
        camera.read()


if __name__ == '__main__':
    main()
