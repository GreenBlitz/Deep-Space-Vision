from exceptions import *
from models import *


def init_send_hatch(camera, conn, stream_camera):
    conn.set('led_f', True)
    conn.set('led_b', True)
    camera.set_exposure(0, foreach=True)
    stream_camera.toggle_auto_exposure(0.75)


def send_hatch(camera, conn):
    ok, frame = camera.read()

    if not ok:
        print(CouldNotReadFrameException("Kinda obvious... Could not read frame"))
        return
    hatches = list(find_hatch(frame, camera))

    if len(hatches) > 0:
        print('found hatch')
        closest_hatch = hatches[0]
        conn.set('x', closest_hatch[0])
        conn.set('y', closest_hatch[1])
        conn.set('z', closest_hatch[2])
        conn.set('angle', closest_hatch[3])
    else:
        print("No hatches were found!")
