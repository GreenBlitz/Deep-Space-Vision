import utils.net as cvnet

from utils import *
from models import *
from vision import find_trash

def main():
    camera = Camera(1, LIFECAM_STUDIO)
    vision_table = cvnet.net_init()
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', frame)
        trash = find_trash(frame, camera)
        vision_table.set('trash x', trash[0])
        vision_table.set('trash y', trash[1])
        vision_table.set('trash z', trash[2])

        vision_table.set('trash norm', np.linalg.norm(trash))

        if cv2.waitKey(1) & 0xff == 27:
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
