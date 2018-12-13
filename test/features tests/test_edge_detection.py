from models import *
from utils import *
from vision import *
import funcs
import drawings


def main():
    camera = Camera(0, LIFECAM_STUDIO)
    time = 0
    while True:
        time += 1
        ok, frame = camera.read()
        thr = funcs.edges(frame)
        thr = funcs.gray(thr)
        thr = cv2.threshold(thr, 5, 255, cv2.THRESH_BINARY)[1]
        thr = cv2.dilate(thr, np.ones((2, 2)))
        cv2.imshow('hello i is vision', thr)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
