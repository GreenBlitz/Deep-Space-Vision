from models import *
from utils import *

rtag = np.array([0, 0, 0, 0])


def find_trash(frame, camera_data):
    global rtag
    rtag = np.array(rtag)
    rects = (threshold_trash + sorted_contours + contours_to_rects_sorted)(frame)

    if len(rects) > 0:
        rtag = rects[0]
    else:
        rects.append(tuple(list(rtag.astype(int))))
    rect = rects[0]
    d = TRASH.location3d_by_params(camera_data, 0.8 * np.sqrt(rect[2] * rect[3]),
                                   (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))

    return d
