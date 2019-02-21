from utils import *
from models import *


def main():
    camera = StreamCamera(0, LIFECAM_3000, None)
    print(camera.im_height)
    print(camera.height)
    camera.resize(0.4, 0.4)
    print(camera.im_height)
    print(camera.height)


if __name__ == '__main__':
    main()
