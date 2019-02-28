import cv2
import numpy as np

import funcs
from .thresholds_consts import *
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
                           lambda frame: cv2.dilate(frame, np.ones((3, 3)), iterations=6))

threshold_hatch_panel = PipeLine(HATCH_PANEL_THRESHOLD,
                                 lambda frame: cv2.erode(frame, np.ones((2, 2)), iterations=1),
                                 lambda frame: cv2.dilate(frame, np.ones((2, 2)), iterations=1))

threshold_vision_target = PipeLine(VISION_TARGET_THRESHOLD)

# lambda frame: cv2.erode(frame, np.ones((2, 2)), iterations=4),
#                                 lambda frame: cv2.dilate(frame, np.ones((5, 5)), iterations=20),
#                                lambda frame: cv2.erode(frame, np.ones((5, 5)), iterations=10))
# CONTOURS

find_contours = PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1])

sort_contours = PipeLine(lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True))

filter_contours = PipeLine((lambda cnts: filter(lambda c: cv2.contourArea(c) >= 3000.0, cnts))) + list

contour_center = PipeLine(lambda cnt: cv2.moments(cnt),
                          lambda m: (int(m['m10'] / (m['m00'] + 0.0000001)), int(m['m01'] / (m['m00'] + 0.0000001))))

contours_centers = PipeLine(lambda cnts: map(contour_center, cnts)) + list

# SHAPES

contours_to_rects = PipeLine(lambda cnts: map(cv2.boundingRect, cnts)) + list

contours_to_rects_sorted = contours_to_rects + (
    lambda rects: sorted(rects, key=lambda x: x[2] * x[3], reverse=True)) + list

contours_to_circles = PipeLine(lambda cnts: map(cv2.minEnclosingCircle, cnts)) + list

contours_to_circles_sorted = contours_to_circles + (
    lambda rects: sorted(rects, key=lambda x: x[1], reverse=True)) + list

contours_to_ellipses = PipeLine(lambda cnts: filter(lambda x: len(x) >= 5, cnts),
                                 # ellipse must get contours of at least five points
                                lambda cnts: map(cv2.fitEllipse, cnts)) + list

contours_to_ellipses_sorted = contours_to_ellipses + (
    lambda elps: sorted(elps, key=lambda x: x[1][0]*x[1][1], reverse=True)) + list


#cv2.cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color[, thickness[, lineType[, shift]]])
#fitEllipse: center,axes,angle,startAngle,endAngle
#contours_to_ellipses = PipeLine(lambda cnts: map(lambda x: (cv2.minEnclosingCircle(x)[0] , (0,0) , 0 , 360.0) if len(x)< 5 else cv2.fitElli

contours_to_rotated_rects = PipeLine(lambda cnts: map(cv2.minAreaRect, cnts)) + list

contours_to_rotated_rects_sorted = contours_to_rotated_rects + PipeLine(
    lambda rects: sorted(rects, key=lambda x: x[1][0] * x[1][1])) + list

contours_to_polygons = PipeLine(lambda cnts: map(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)), cnts),
                                lambda cnts: map(lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                                                 cnts),
                                lambda polydps: map(lambda polydp: map(lambda x: x[0], polydp), polydps),
                                lambda polydps: map(lambda polydp: list(map(tuple, polydp)), polydps)) + list

filter_inner_circles = PipeLine(funcs.filter_inner_circles)

filter_inner_rects = PipeLine(funcs.filter_inner_rects)
