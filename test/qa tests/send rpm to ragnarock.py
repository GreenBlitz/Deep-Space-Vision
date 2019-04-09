from utils.net import *
from utils import *
from models import *
from vision import *

SHOOTER_ANGLE = np.deg2rad(69)  # lol
GRAVITY_CONSTANT = 9.8


def main():
    camera = Camera(PORT, LIFECAM_STUDIO)
    camera.set_exposure(1)
    table_conn = net_init(ip='10.45.90.2')
    k = 500

    while True:
        ok, frame = camera.read()
        trash = find_trash(frame, camera)
        trash_distance = np.linalg.norm(trash)
        trash_angle = np.rad2deg(np.arctan(trash[0] / trash[2]))
        cv2.imshow('feed', frame)
        cv2.imshow('threshold', TRASH_THRESHOLD(frame))
        table_conn.set('Trash::Distance', trash_distance)
        desired_speed = trash[2] / (np.cos(SHOOTER_ANGLE) * np.sqrt(
            (2 / GRAVITY_CONSTANT) * (np.tan(SHOOTER_ANGLE) * trash[2] + trash[1])))  # beautifulMath.exe
        desired_rpm = (desired_speed / (0.20 * 2 * np.pi)) * 60
        table_conn.set('Trash::RPM', desired_rpm)
        table_conn.set('Trash::Angle', trash_angle)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
