from exceptions import *
import time
from models import *

last_found = 0
start_time = -1


def send_cargo(camera, conn):
    global last_found
    global start_time

    if start_time == -1:
        start_time = time.clock()

    ok, frame = camera.read()

    if not ok:
        raise CouldNotReadFrameException("Kinda obvious... Could not read frame")
    cargos = list(find_cargo(frame, camera))
    last_found += 1
    if last_found > 5:
        conn.set('cargo::distance', 0)
        conn.set('cargo::angle', 0)
    if len(cargos) > 0:
        print('found_cargo')
        last_found = 0
        closest_cargo = cargos[0]
        dist = np.linalg.norm(closest_cargo)
        angle = np.rad2deg(np.arctan(closest_cargo[0]/closest_cargo[2]))
        conn.set('cargo::distance', dist)
        conn.set('cargo::angle', angle)

        if time.clock() - start_time > 1:
            print(cargos)
            print("angle: {angle}, distance: {dist}".format(angle=angle, dist=dist))
            start_time = time.clock()
    else:
        print("No cargo was found!")
