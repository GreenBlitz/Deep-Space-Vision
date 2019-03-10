from models import *
from utils import *
from utils.net import *

current_threshold = threshold_vision_target


def main():
    camera = StreamClient("10.45.90.8", port=5801)
    while True:
        frame = camera.get_frame()
        cv2.imshow("feed", frame)
        cv2.imshow("threshold", current_threshold(frame))
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
