from utils import *
from models import *
from exceptions import CouldNotReadFrameException


def send_hatch(camera, conn):
    ok, frame = camera.read()
    if not ok:
        raise CouldNotReadFrameException("Kinda obvious... Could not read frame")
    hatches = list(find_hatch(frame, camera))
    if len(hatches) > 0:
        closest_hatch = hatches[0]
        conn.set('hatch::distance', np.linalg.norm(closest_hatch))
        conn.set('hatch::angle', np.rad2deg(np.arctan(closest_hatch[0]/closest_hatch[2])))
