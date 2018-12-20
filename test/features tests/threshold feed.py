from models import *
from utils import *

current_threshold = TRASH_THRESHOLD


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
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
