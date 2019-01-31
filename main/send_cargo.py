from utils import *
from models import *
from exceptions import CouldNotReadFrameException
last_found = 0

def send_cargo(camera, conn):
    global last_found
    ok, frame = camera.read()
    if not ok:
        raise CouldNotReadFrameException("Kinda obvious... Could not read frame")
    cargos = list(find_cargo(frame, camera))
    last_found += 1
    if last_found > 5:
        conn.set('cargo::distance', 1)
        conn.set('cargo::angle', 0)
    if len(cargos) > 0:
        last_found = 0
        print(cargos)
        closest_cargo = cargos[0]
        dist = np.linalg.norm(closest_cargo)
        angle = np.rad2deg(np.arctan(closest_cargo[0]/closest_cargo[2]))
        conn.set('cargo::distance', dist)
        conn.set('cargo::angle', angle)
        print("angle: {angle}, distance: {dist}".format(angle=angle, dist=dist))
    else:
        print("No cargo was found!")
