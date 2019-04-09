from utils import *
from models import *


def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.set_exposure(-13)
    hatch = np.array([0.0, 0.0, 0.0])
    while True:
        ok, frame = camera.read()
        targets = list(find_vision_target(frame, camera))
        if len(targets) >= 2:
            hatch = (targets[0] + targets[1])/2
        cv2.imshow('feed', frame)
        cv2.imshow('threshold', threshold_vision_target(frame))
        k = cv2.waitKey(1) & 0xff
        if k == ord('d'):
            print(np.linalg.norm(hatch))
        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
