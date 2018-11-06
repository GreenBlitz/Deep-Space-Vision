from utils import *
from models import *

SQRT_PI = np.sqrt(np.pi)


def find_fuels(frame, camera_data):
    """
    get coordinates and distance of all balls
    """
    circles = find_fuel_circles()
    d = []
    if len(cnts) > 0:
        for cnt in cnts:
            center, r = cv2.minEnclosingCircle(cnt)
            area = SQRT_PI*r
            d.append(FUEL.location3d_by_params(camera_data, area, center))
    return d

