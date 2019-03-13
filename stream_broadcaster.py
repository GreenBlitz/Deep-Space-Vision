from utils.net import TCPStreamServer
from utils import StreamCamera
from models import LIFECAM_3000


def main():
    server = TCPStreamServer(ip='0.0.0.0', port=5801, fx=0.5, fy=0.5, max_fps=22)
    camera = StreamCamera(0, LIFECAM_3000, server, should_stream=True)
    while True:
        ok, frame = camera.read()


if __name__ == '__main__':
    main()
