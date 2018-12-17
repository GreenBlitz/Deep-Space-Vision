from utils import *
from models import *

current_threshold = Threshold([[40.46404285229044, 54.679546252804016],
                               [78.49554118824669, 141.7333240444942],
                               [86.49577698856463, 230.71946868865734]], 'HLS')


def main():
    camera = Camera(0, LIFECAM_STUDIO)
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
