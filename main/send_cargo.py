from utils import *
from models import *
from exceptions import CouldNotReadFrameException


def send_cargo(camera, conn):
    ok, frame = camera.read()
    if not ok:
        raise CouldNotReadFrameException("Kinda obvious... Could not read frame")
    cargos = list(find_cargo(frame, camera))
    if len(cargos) > 0:
        print(cargos)
        closest_cargo = cargos[0]
        conn.set('cargo::distance', np.linalg.norm(closest_cargo))
        conn.set('cargo::angle', np.rad2deg(np.arctan(closest_cargo[0]/closest_cargo[2])))
