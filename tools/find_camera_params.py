import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture(1)
    while True:
        ok, frame = cap.read()
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('r'):
            box = cv2.selectROI('feed', frame)
            print(box)
            width, height = float(raw_input('enter width in meters: ')), float(raw_input('enter height in meters: '))
            distance = float(raw_input('enter distance in meters: '))
            print(np.sqrt((box[2]*box[3])/(width*height))*distance)
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
