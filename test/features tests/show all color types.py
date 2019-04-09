from utils import *
from models import *


def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.set_exposure(-6)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', frame)
        cv2.imshow('hls', cv2.cvtColor(frame, cv2.COLOR_BGR2HLS))
        cv2.imshow('hsv', cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
        cv2.imshow('luv', cv2.cvtColor(frame, cv2.COLOR_BGR2LUV))
        cv2.imshow('lab', cv2.cvtColor(frame, cv2.COLOR_BGR2LAB))
        cv2.imshow('yuv', cv2.cvtColor(frame, cv2.COLOR_BGR2YUV))
        cv2.imshow('xyz', cv2.cvtColor(frame, cv2.COLOR_BGR2XYZ))
        cv2.imshow('ycr_cb', cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB))
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
