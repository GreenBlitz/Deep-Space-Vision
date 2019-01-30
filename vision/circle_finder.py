from .object_finder import ObjectFinder
from models import *


class CircleFinder(ObjectFinder):
    def __init__(self, threshold_func, object_descriptor):
        ObjectFinder.__init__(self, threshold_func, object_descriptor)
        self.__full_pipeline = (threshold_func +
                                find_contours + 
                                filter_contours +
                                sort_contours + 
                                contours_to_circles_sorted +
                                filter_inner_circles)

    def __call__(self, frame, camera):
        circles = self.__full_pipeline(frame)
        return map(lambda circ: self.im_object.location3d_by_params(camera, SQRT_PI*circ[1], circ[0]), circles)
        #d = []
        #for circ in circles:
        #    center, r = circ
        #    area = SQRT_PI * r
        #    d.append(self.im_object.location3d_by_params(camera, area, center))
        #return d
