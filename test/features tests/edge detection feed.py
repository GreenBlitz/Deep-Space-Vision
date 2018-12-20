from funcs import *
from models import LIFECAM_STUDIO, PORT
from utils import *


def fix_img255(im):
    # return 255*(im/np.amax(im))
    return gray(im)


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    while True:
        ok, frame = camera.read()
        cv2.imshow("feed", frame)
        cv2.imshow("edges", fix_img255(edges(frame)))
        cv2.imshow("corners", fix_img255(corners(frame)))
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
