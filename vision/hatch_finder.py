from .rotated_rect_finder import RotatedRectFinder
from models import *
from funcs import *

ENCLOSING_RECT_MAX_RATIO = 0.549719211778


class HatchFinder(RotatedRectFinder):
    def __init__(self, threshold_func, object_descriptor, vt_distance=0.2866, area_scalar=1.0):
        RotatedRectFinder.__init__(self, threshold_func, object_descriptor, area_scalar)
        self.__vector_distance = np.array([vt_distance/2, 0, 0])
        self.vt_distance = vt_distance

    def __call__(self, frame, camera):
        rects = self.__full_pipeline(frame)

        left_targets, right_targets = split_list(
            lambda rotated_rect: rotated_rect[2] < 0 or rotated_rect[2] > np.pi, rects)

        left_targets_real, right_targets_real = [], []
        for i in left_targets:
            left_targets_real.append(self.im_object.location3d_by_params(np.sqrt(i[1][0] * i[1][1]), i[0]))
        for i in left_targets:
            left_targets_real.append(self.im_object.location3d_by_params(np.sqrt(i[1][0] * i[1][1]), i[0]))

        target_pairs = []
        i = 0
        while i < len(left_targets_real):
            lt = left_targets_real[i]
            possibles = sorted(filter(lambda t: abs(np.linalg.norm(lt - t[1]) - self.vt_distance) < 0.1,
                                      (zip(range(len(right_targets_real)), right_targets_real))),
                               key=lambda t: abs(np.linalg.norm(lt - t[1]) - self.vt_distance))
            for p in possibles:
                if right_targets[p[0]][0][0] > left_targets[i][0][0]:
                    target_pairs.append((lt, p[1]))
                    del left_targets[i]
                    del left_targets_real[i]
                    del right_targets[p[0]]
                    del right_targets_real[p[0]]
                    i -= 1
                    break
            i += 1
        all_hatches = []
        for i in target_pairs:
            all_hatches.append((i[0] + i[1]) / 2)

        for i, t in enumerate(left_targets_real):
            width, height = left_targets[i][1]
            w_s = np.cos(left_targets[i][2]) * width + np.sin(left_targets[i][2]) * height
            h_s = np.sin(left_targets[i][2]) * width + np.cos(left_targets[i][2]) * height
            angle = np.arccos(min(w_s / h_s, h_s / w_s) / ENCLOSING_RECT_MAX_RATIO)
            rot_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                   [0, 1, 0],
                                   [-np.cos(angle), 0, np.cos(angle)]])
            all_hatches.append(t + rot_matrix.dot(self.__vector_distance))

        for i, t in enumerate(right_targets_real):
            width, height = right_targets[i][1]
            w_s = np.cos(right_targets[i][2]) * width + np.sin(right_targets[i][2]) * height
            h_s = np.sin(right_targets[i][2]) * width + np.cos(right_targets[i][2]) * height
            angle = np.arccos(min(w_s / h_s, h_s / w_s) / ENCLOSING_RECT_MAX_RATIO)
            rot_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                   [0, 1, 0],
                                   [-np.cos(angle), 0, np.cos(angle)]])
            all_hatches.append(t - rot_matrix.dot(self.__vector_distance))
        all_hatches.sort(key=lambda v: np.linalg.norm(v))
        return all_hatches
