from utils import *
from models import *
from utils.net import *


def main():
    camera = StreamCamera(PORT, LIFECAM_3000, TCPStreamClient(ip='127.0.0.1'))

    camera.toggle_stream(True)
    camera.resize(0.4, 0.4)
    while True:
        ok, frame = camera.read()
        cv2.imshow('threshold', threshold_cargo(frame))
        print(np.linalg.norm(np.array(list(find_cargo(frame, camera)))))
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
