from models import *


def find_fuels(frame, camera_data):
    """
    get coordinates and distance of all balls
    """
    circles = find_fuel_circles(frame)
    d = []

    for circ in circles:
        center, r = circ
        area = SQRT_PI * r
        d.append(FUEL.location3d_by_params(camera_data, area, center))
    return d
