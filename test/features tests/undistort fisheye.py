from models import *
from utils import *

def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.set_exposure(-5)
    while True:
        ok, frame = camera.read()
        cv2.imshow("feed", frame)
        cv2.imshow("undistorted", cv2.fisheye.undistortImage(frame, 5, 5, 5))
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
