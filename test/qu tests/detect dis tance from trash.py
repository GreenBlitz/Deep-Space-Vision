import utils.net as cvnet
from models import *
from utils import *
from vision import find_trash


def main():
    camera = Camera(1, LIFECAM_STUDIO)
    vision_table = cvnet.net_init()
    camera.set(cv2.CAP_PROP_EXPOSURE, 1)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', frame)
        trash = find_trash(frame, camera)
        vision_table.set('trash x', trash[0])
        vision_table.set('trash y', trash[1])
        vision_table.set('trash z', trash[2])

        vision_table.set('Trash::Distance', np.linalg.norm(trash))
        vision_table.set('Trash::Angle', np.rad2deg(np.arctan(trash[0] / trash[2])))

        if cv2.waitKey(1) & 0xff == 27:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
