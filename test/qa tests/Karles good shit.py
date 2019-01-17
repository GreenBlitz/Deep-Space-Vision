import utils.net as cvnet
from models import *
from utils import *

DISTANCE_FROM_BALL_HALL_TO_VISION_TARGETS = 5

def main():
    camera = Camera(PORT, MICROSOFT_CAM)
    camera.set_exposure(-13)
    vision_table = cvnet.net_init()
    camera.set(cv2.CAP_PROP_EXPOSURE, 1)
    while True:

        ok, frame = camera.read()
        cv2.imshow('feed', frame)

        hatch = find_hatch(frame, camera)

        vision_table.set('Target::Distance', np.linalg.norm(hatch))
        vision_table.set('Target::Angle', np.rad2deg(np.arctan2(hatch[2], hatch[0])))

        if cv2.waitKey(1) & 0xff == 27:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()


def find_center(frame):  # rename it please
