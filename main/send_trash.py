from utils import *
from models import *


def send_trash(camera, conn):
    ok, frame = camera.read()

    trashes = list(find_trash(frame, camera))
    if len(trashes) > 0:
        trash = trashes[0]
        print(trash)
        conn.set('trash::distance', np.linalg.norm(trash))
        conn.set('trash::angle', np.rad2deg(np.arctan(trash[0] / trash[2])))
