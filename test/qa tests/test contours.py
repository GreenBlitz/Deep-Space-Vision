from utils import *
from models import *


def main():
    camera = Camera(0, LIFECAM_3000)
    while True:
        ok, frame = camera.read()
        thr = threshold_cargo(frame)
        contours = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(contours)
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) & 0xff == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
