from .object_finder import ObjectFinder
from models import *


class RectFinder(ObjectFinder):
    def __init__(self, threshold_func, object_descriptor, area_scalar=1.0):
        ObjectFinder.__init__(self, threshold_func, object_descriptor)
        self.__full_pipeline = (threshold_func +
                                find_contours + 
                                filter_contours +
                                sort_contours +
                                contours_to_rects_sorted)
        self.area_scalar = area_scalar

    def __call__(self, frame, camera):
        rects = self.__full_pipeline(frame)
        return map(
            lambda rect: self.im_object.location3d_by_params(camera, self.area_scalar * np.sqrt(rect[2] * rect[3]),
                                                             [(rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2]), rects)
        #d = []
        #for rect in rects:
        #    area = self.area_scalar * np.sqrt(rect[2] * rect[3])
        #    center = [(rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2]
        #    d.append(self.im_object.location3d_by_params(camera, area, center))
        #return d
