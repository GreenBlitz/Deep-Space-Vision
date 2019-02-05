from models import *
from utils import *

current_threshold = threshold_cargo


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    camera.resize(0.25, 0.25)
    import os
    os.system('v4l2-ctl -d /dev/video0 -c exposure_auto=1')
    camera.set_exposure(-5)
    while True:
        ok, frame = camera.read()
        cv2.imshow("feed", frame)
        cv2.imshow("threshold", current_threshold(frame))
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
