import cv2
import numpy as np
from models import *
from utils import *


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    i = 7
    while True:
        ok, frame = camera.read()
        cv2.imshow("feed", frame)
        k = cv2.waitKey(1) & 0xFF
        if ord('Z') >= k >= ord('A'):
            k += ord('a') - ord('A')
        if k == ord("i"):
            cv2.imwrite("Vision" + str(i) + ".bmp", frame)
            i += 1
        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
