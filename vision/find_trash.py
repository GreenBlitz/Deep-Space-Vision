from models import *
from utils import *


def find_trash(frame, camera_data):
    rect = np.array([0, 0, 0, 0])
    rects = (threshold_trash + sorted_contours + contours_to_rects_sorted)(frame)

    if len(rects) > 0:
        rect = rects[0]
    d = TRASH.location3d_by_params(camera_data, 0.8 * np.sqrt(rect[2] * rect[3]),
                                   (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))

    return d
