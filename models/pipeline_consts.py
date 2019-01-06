import cv2
import numpy as np

import funcs
from thresholds_consts import *
from utils.pipeline import PipeLine

# THRESHOLDS

threshold_fuel = PipeLine(FUEL_THRESHOLD,
                          lambda frame: cv2.erode(frame, np.ones((3, 3))),
                          lambda frame: cv2.dilate(frame, np.ones((3, 3)), iterations=4))

threshold_trash = PipeLine(TRASH_THRESHOLD,
                           lambda frame: cv2.erode(frame, np.ones((3, 3)), iterations=2),
                           lambda frame: cv2.dilate(frame, np.ones((3, 3)), iterations=25),
                           lambda frame: cv2.erode(frame, np.ones((2, 2)), iterations=10))

threshold_cargo = PipeLine(CARGO_THRESHOLD,
                           lambda frame: cv2.erode(frame, np.ones((3, 3)), iterations=2),
                           lambda frame: cv2.dilate(frame, np.ones((3, 3)), iterations=2))

threshold_hatch_panel = PipeLine(HATCH_PANEL_THRESHOLD,
                                 lambda frame: cv2.erode(frame, np.ones((3, 3))),
                                 lambda frame: cv2.dilate(frame, np.ones((5, 5)), iterations=3))

# lambda frame: cv2.erode(frame, np.ones((2, 2)), iterations=4),
#                                 lambda frame: cv2.dilate(frame, np.ones((5, 5)), iterations=20),
#                                lambda frame: cv2.erode(frame, np.ones((5, 5)), iterations=10))
# CONTOURS

find_contours = PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1])

sort_contours = PipeLine(lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True))

filter_contours = PipeLine((lambda cnts: filter(lambda c: cv2.contourArea(c) >= 300.0, cnts)))

contour_center = PipeLine(lambda cnt: cv2.moments(cnt),
                          lambda m: (int(m['m10'] / (m['m00'] + 0.0000001)), int(m['m01'] / (m['m00'] + 0.0000001))))

# SHAPES

contours_to_rects = PipeLine(lambda cnts: map(lambda x: cv2.boundingRect(x), cnts))

contours_to_rects_sorted = contours_to_rects + (lambda rects: sorted(rects, key=lambda x: x[2] * x[3], reverse=True))

contours_to_circles = PipeLine(lambda cnts: map(lambda x: cv2.minEnclosingCircle(x), cnts))

contours_to_circles_sorted = contours_to_circles + (lambda rects: sorted(rects, key=lambda x: x[1], reverse=True))

contour_to_polygon = PipeLine(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)),
                              lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                              lambda polydp: map(lambda x: x[0], polydp),
                              lambda polydp: map(tuple, polydp))

filter_inner_circles = PipeLine(funcs.filter_inner_circles)
