import cv2
from utils import *
from models import *


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    while True:
        ok, frame = camera.read()
        circles = cv2.HoughCircles(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.HOUGH_GRADIENT, 1.2, 200)

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        cv2.imshow('feed', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
