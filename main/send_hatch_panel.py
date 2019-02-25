from exceptions import *
from models import *


def init_send_hatch_panel(camera, conn):
    conn.set('led_f', False)
    conn.set('led_b', False)
    camera.toggle_auto_exposure(0.25, foreach=True)
    camera.set_exposure(1, foreach=True)


def send_hatch_panel(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    hatches = list(find_hatch_panel(frame, camera))

    if len(hatches) > 0:
        closest_panel = CAMERA_ROTATION_MATRIX.dot(hatches[0])
        conn.set('output', list(closest_panel) + [0.0])
