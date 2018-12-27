import utils.net as cvnet
from models import *
from utils import *
from vision import find_trash


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    vision_table = cvnet.net_init()
    camera.set(cv2.CAP_PROP_EXPOSURE, 1)
    time = 0
    d = 0
    while True:

        time += 1
        ok, frame = camera.read()

        cv2.imshow('feed', frame)
        cv2.imshow('threashhold', TRASH_THRESHOLD(frame))
        trash = find_trash(frame, camera)

        vision_table.set('trash x', trash[0])
        vision_table.set('trash y', trash[1])
        vision_table.set('trash z', trash[2])
        vision_table.set('Trash::Angle', np.rad2deg(np.arctan(trash[0] / trash[2])))
        distance = np.linalg.norm(trash)

        if distance >= 6:
            distance = 0

        vision_table.set('Trash::Distance', distance)

        if np.abs(d - np.linalg.norm(trash)) >= 0.15:
            print "Trash distance is: " + str(np.linalg.norm(trash)) + " meters"

        d = np.linalg.norm(trash)

        if cv2.waitKey(1) & 0xff == 27:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
