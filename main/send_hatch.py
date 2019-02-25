from exceptions import *
from models import *


def init_send_hatch(camera, conn):
    conn.set('led_f', True)
    conn.set('led_b', True)
    camera.toggle_auto_exposure(0.25, foreach=True)
    camera.set_exposure(0, foreach=True)


def send_hatch(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    hatches = list(find_hatch(frame, camera))

    if len(hatches) > 0:
        closest_hatch = hatches[0]
        closest_hatch[0:3] = CAMERA_ROTATION_MATRIX.dot(closest_hatch[0:3])
        print('closest hatch: %s' % str(closest_hatch))
        conn.set('output', list(closest_hatch))
