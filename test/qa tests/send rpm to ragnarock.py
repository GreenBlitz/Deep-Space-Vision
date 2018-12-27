from utils.net import *
from utils import *
from models import *
from vision import *


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    camera.set_exposure(1)
    table_conn = net_init(ip='10.45.90.2')
    k = 500

    while True:
        ok, frame = camera.read()
        trash = find_trash(frame, camera)
        trash_distance = np.linalg.norm(trash)
        alpha = k*trash_distance + 50;
        trash_angle = np.rad2deg(np.arctan(trash[0]/trash[2]))
        cv2.imshow('feed', frame)
        cv2.imshow('threshold', TRASH_THRESHOLD(frame))
        table_conn.set('Trash::Distance', trash_distance)
        desired_rpm = alpha * trash_distance
        table_conn.set('Trash::RPM', desired_rpm)
        table_conn.set('Trash::Angle', trash_angle)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break
        if k == ord('u'):
            print 'old alpha -> %d' % alpha
            alpha = float(raw_input('new alpha -> '))


if __name__ == '__main__':
    main()
