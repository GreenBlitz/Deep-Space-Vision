from utils.pipeline import PipeLine
from thresholds import *
import numpy as np

threshold_fuel = PipeLine(FUEL_THRESHOLD,
                          lambda frame: cv2.erode(frame, np.ones((3, 3))),
                          lambda frame: cv2.dilate(frame, np.ones((3, 3)), iterations=4))

threshold_trash = PipeLine(TRASH_THRESHOLD,
                           lambda frame: cv2.erode(frame, np.ones((5, 5))),
                           lambda frame: cv2.dilate(frame, np.ones((3, 3)), iterations=5))

sorted_contours = PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1],
                           lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True))

fuel_contours = threshold_fuel + sorted_contours

fuel_contours_filtered = fuel_contours + (lambda cnts: filter(lambda c: cv2.contourArea(c) >= 300.0, cnts))

trash_contours = threshold_trash + sorted_contours

trash_contours_filtered = fuel_contours + (lambda cnts: filter(lambda c: cv2.contourArea(c) >= 300.0, cnts))

contour_to_polygon = PipeLine(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)),
                              lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                              lambda polydp: map(lambda x: x[0], polydp),
                              lambda polydp: map(tuple, polydp))

contour_center = PipeLine(lambda cnt: cv2.moments(cnt),
                          lambda m: (int(m['m10']/(m['m00'] + 0.0000001)), int(m['m01']/(m['m00'] + 0.0000001))))


