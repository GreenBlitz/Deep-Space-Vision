from utils.net import *
from utils import *
from models import *
from vision import *


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    table_conn = net_init()
    alpha = 900/2.53

    while True:
        ok, frame = camera.read()
        trash = find_trash(frame, camera)
        trash_distance = np.linalg.norm(trash)
        cv2.imshow('feed', frame)
        table_conn.set('Trash::Distance', trash_distance)
        desired_rpm = alpha * trash_distance
        print desired_rpm
        table_conn.set('Trash::DesiredRPM', desired_rpm)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
