from utils import *
from models import *
from funcs import *
from exceptions import *

ENCLOSING_RECT_MAX_RATIO = 0.549719211778

vt_distance = 0.2866


def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.toggle_auto_exposure(0)
    print('[DEBUG] changed camera exposure' if camera.set_exposure(-13) else '[WARN] unable to set camera exposure')
    target_to_rotated_rects = (threshold_vision_target +
                               (lambda frame: cv2.medianBlur(frame, 7)) +
                               find_contours +
                               filter_contours +
                               sort_contours)

    while True:
        ok, frame = camera.read()
        if not ok:
            raise CouldNotReadFrameException()
        cv2.imshow('threshold', (threshold_vision_target + (lambda frame: cv2.medianBlur(frame, 7)))(frame))
        cnts = target_to_rotated_rects(frame)
        rects = contours_to_rotated_rects(cnts)
        polys = contours_to_polygons(cnts)
        rects_polys = zip(rects, polys)
        left_targets_polys, right_targets_polys = split_list(
            lambda rotated_rect: rotated_rect[0][2] < -45.0, rects_polys)

        left_targets = list(map(lambda pair: pair[0], left_targets_polys))
        right_targets = list(map(lambda pair: pair[0], right_targets_polys))

        left_targets_real, right_targets_real = [], []
        for i in left_targets:
            left_targets_real.append(VISION_TARGET.location3d_by_params(camera, np.sqrt(i[0] * i[1]), [i[0], i[2]]))
        for i in right_targets:
            right_targets_real.append(VISION_TARGET.location3d_by_params(camera, np.sqrt(i[0] * i[1]), [i[0], i[2]]))

        target_pairs = []
        i = 0
        while i < len(left_targets_real):
            lt = left_targets_real[i]
            possibles = sorted(filter(lambda t: abs(np.linalg.norm(lt - t[1]) - vt_distance) < 0.2,
                                      enumerate(right_targets_real)),
                               key=lambda t: abs(np.linalg.norm(lt - t[1]) - vt_distance))
            for p in possibles:
                if right_targets[p[0]][0][0] < left_targets[i][0][0]:
                    target_pairs.append((lt, p[1]))
                    del left_targets[i]
                    del left_targets_real[i]
                    del left_targets_polys[i]
                    del right_targets[p[0]]
                    del right_targets_real[p[0]]
                    del right_targets_polys[p[0]]
                    i -= 1
                    break
            i += 1
        all_hatches = []
        for i in target_pairs:
            all_hatches.append(
                np.concatenate(((i[0] + i[1]) / 2,
                                np.array([np.arccos(max(-1, min(1, (i[0][2] - i[1][2]) / vt_distance)))]))))


        cv2.imshow('feed', frame)

        k = cv2.waitKey(1) & 0xff

        if k == ord('d'):
            print(all_hatches[0][3] if len(all_hatches) > 0 else None)
            print(all_hatches[1][3] if len(all_hatches) > 1 else None)

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
