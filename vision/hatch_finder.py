from .object_finder import ObjectFinder
from models import *


class HatchFinder(ObjectFinder):
    def __init__(self, distance):
        ObjectFinder.__init__(self, 0, 0)
        self.distance = distance
        self.__vector_distance = np.array([0, distance, 0])

    def __call__(self, frame, camera):
        try:
            polys = (threshold_vision_target + find_contours + filter_contours + sort_contours + contours_to_polygons)(
                frame)
            poly1, poly2 = polys[0], polys[1]
            poly1 = sorted(poly1, key=lambda point: point[1])
            poly2 = sorted(poly2, key=lambda point: point[1])
            if abs(poly2[1][0] - poly1[1][0]) > abs(poly1[2][0] - poly2[2][0]):
                return None
            vision_target1, vision_target2 = find_vision_target(frame, camera)[:2]

            return (vision_target1 + vision_target2) / 2 - self.__vector_distance

        except Exception as e:
            print(e)
            return None
