from models import *
from utils import *

rtag = np.array([0, 0, 0, 0])


def find_trash(frame, camera_data):
    thr = threshold_trash(frame)
    cnts = sorted_contours(thr)
    rects = contours_to_rects_sorted(cnts)

    if len(rects) > 0:
        if rects[0][2]*rects[0][3] < globals()['rtag'][3]*globals()['rtag'][2]:
            globals()['rtag'] = 0.8*globals()['rtag'] + 0.2*np.array(rects[0])
            rects[0] = tuple(list(globals()['rtag'].astype(int)))
        else:
            globals()['rtag'] = rects[0]
    else:
        rects.append(tuple(list(globals()['rtag'].astype(int))))
    d = TRASH.distance_by_params(camera_data, 0.8*np.sqrt(rects[0][2]*rects[0][3]))

    return d, rects[0]
