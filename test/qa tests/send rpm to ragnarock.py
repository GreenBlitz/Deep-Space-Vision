from utils.net import *
from utils import *
from models import *
from vision import *


def main():
    camera = Camera(0, LIFECAM_STUDIO)
    table_conn = net_init()
    alpha_delta_are_the_best_alpha = 100
    while True:
        ok, frame = camera.read()
        trash = find_trash(frame, camera)
        trash_distance = np.linalg.norm(trash)
        table_conn.set('Trash::Distance', trash_distance)
        desired_rpm = alpha_delta_are_the_best_alpha*trash_distance
        table_conn.set('Trash::DesiredRPM', desired_rpm)


if __name__ == '__main__':
    main()
