from exceptions import *
from models import *


def init_send_cargo(camera, conn):
    conn.set('led_f', False)
    conn.set('led_b', False)
    camera.set_exposure(1, foreach=True)


def send_cargo(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    cargos = list(find_cargo(frame, camera))

    if len(cargos) > 0:
        print('found_cargo')
        closest_cargo = cargos[0]
        conn.set('x', closest_cargo[0])
        conn.set('y', closest_cargo[1])
        conn.set('z', closest_cargo[2])
        conn.set('angle', 0)
    else:
        print("No cargo was found!")
