from models import *
from utils import *

current_threshold = threshold_hatch_panel

def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    camera.set_exposure(-6)
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
