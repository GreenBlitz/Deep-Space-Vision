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
        conn.set('x', closest_hatch[0])
        conn.set('y', closest_hatch[1])
        conn.set('z', closest_hatch[2])
        conn.set('angle', 0)
    else:
        print("Not enough hatches were found!")
