from exceptions import *
from models import *


def init_send_hatch_panel(camera, conn):
    conn.set('led_f', False)
    conn.set('led_b', False)
    camera.set_exposure(1, foreach=True)


def send_hatch_panel(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    hatches = list(find_hatch_panel(frame, camera))

    if len(hatches) > 0:
        print('found hatch')
        closest_hatch = hatches[0]
        conn.set('x', closest_hatch[0])
        conn.set('y', closest_hatch[1])
        conn.set('z', closest_hatch[2])
        conn.set('angle', 0)
    else:
        print("No hatches were found!")
