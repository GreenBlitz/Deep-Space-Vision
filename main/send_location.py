from exceptions import *
from models import *


def init_send_location(camera, conn):
    conn.set('led_f', True)
    conn.set('led_b', True)
    camera.set_exposure(0, foreach=True)


def send_location(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    hatches = list(find_hatch(frame, camera))

    if len(hatches) > 1:
        print('found hatches')
        closest_hatch_1, closest_hatch_2 = hatches[:2]
        closest_hatch = (closest_hatch_1 + closest_hatch_2) / 2
        closest_hatch[0:3] = CAMERA_ROTATION_MATRIX.dot(closest_hatch[0:3])
        conn.set('output', list(closest_hatch))
