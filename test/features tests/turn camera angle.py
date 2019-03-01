from utils import *
from models import *


def main():
    camera = Camera(0, LIFECAM_3000)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', frame)

        framet = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow('90 clockwise', framet)

        framet = cv2.rotate(frame, cv2.ROTATE_180)
        cv2.imshow('180', framet)

        framet = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imshow('90 counter clockwise', framet)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
