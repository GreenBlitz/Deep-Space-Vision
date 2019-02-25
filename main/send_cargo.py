from exceptions import *
from models import *


def init_send_cargo(camera, conn):
    conn.set('led_f', False)
    conn.set('led_b', False)
    camera.toggle_auto_exposure(0.25, foreach=True)
    camera.set_exposure(1, foreach=True)


def send_cargo(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    cargos = list(find_cargo(frame, camera))

    if len(cargos) > 0:
        closest_cargo = CAMERA_ROTATION_MATRIX.dot(cargos[0])
        conn.set('output', list(closest_cargo) + [0.0])
