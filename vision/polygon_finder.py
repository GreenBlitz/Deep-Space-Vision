from .object_finder import ObjectFinder
from models import *


class PolygonFinder(ObjectFinder):
    def __init__(self, threshold_func, object_descriptor, area_scalar=1.0):
        ObjectFinder.__init__(self, threshold_func, object_descriptor)
        self.__full_pipeline = (threshold_func +
                                filter_contours +
                                sort_contours)
        self.area_scalar = area_scalar

    def __call__(self, frame, camera):
        contours = self.__full_pipeline(frame)
        return map(
            lambda cnt: self.im_object.location3d_by_params(camera, self.area_scalar * np.sqrt(cv2.contourArea(cnt)),
                                                            contour_center(cnt)), contours)