from exceptions import *
from models import *


def init_send_hatch_panel(camera, conn, leds):
    leds.off()
    camera.toggle_stream(True, foreach=True)
    camera.toggle_auto_exposure(0.25, foreach=True)
    camera.set_exposure(1, foreach=True)


def send_hatch_panel(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    hatches = list(find_hatch_panel(frame, camera))
    conn.set('found', len(hatches) > 0)
    if len(hatches) > 0:
        closest_panel = CAMERA_ROTATION_MATRIX.dot(hatches[0])
        conn.set('output', list(closest_panel) + [0.0])
