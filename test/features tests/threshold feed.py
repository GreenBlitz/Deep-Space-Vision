from models import *
from utils import *

current_threshold = threshold_vision_target


def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.set_exposure(-13)
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
