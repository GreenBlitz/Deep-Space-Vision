from models import *
from utils import *

def send_fuel(camera, conn):
    ok, frame = camera.read()
    
    if not ok:
        pass # raise VisionException()

    fuels = list(find_fuels(frame, camera))
    if len(fuels) > 0:
        c_fuel = fuels[0]
        conn.set('fuel::distance', np.linalg.norm(c_fuel))
        conn.set('fuel::angle', np.rad2deg(np.arctan(c_fuel[0]/c_fuel[2])))

