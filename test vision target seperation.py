from utils import *
from models import *
from funcs import *
from exceptions import *

ENCLOSING_RECT_MAX_RATIO = 0.549719211778


def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.resize(0.5, 0.5)
    camera.toggle_auto_exposure(0.25)
    print('[DEBUG] changed camera exposure' if camera.set_exposure(0) else '[WARN] unable to set camera exposure')
    target_to_rotated_rects = (threshold_vision_target +
                               (lambda frame: cv2.medianBlur(frame, 13)) + 
                               find_contours +
                               filter_contours +
                               sort_contours)

    while True:
        ok, frame = camera.read()
        if not ok:
            raise CouldNotReadFrameException()
        cv2.imshow('threshold', (threshold_vision_target + (lambda frame: cv2.medianBlur(frame, 13)))(frame))
        cnts = target_to_rotated_rects(frame)

        rects = contours_to_rotated_rects(cnts)
        polys = list(contours_to_polygons(cnts))

        #print(polys)
        rects_polys = zip(rects, polys)

        left_targets, right_targets = split_list(
            lambda rotated_rect: rotated_rect[0][2] < -45, rects_polys)

        for i in left_targets:
           cv2.drawContours(frame, [np.int0(cv2.boxPoints(i[0]))], 0, (255, 0, 0), 2)
        for i in right_targets:
           cv2.drawContours(frame, [np.int0(cv2.boxPoints(i[0]))], 0, (0, 0, 255), 2)

        left_targets_real, right_targets_real = [], []

        for i in left_targets:
            left_targets_real.append(VISION_TARGET.location3d_by_params(camera, np.sqrt(i[0][1][0] * i[0][1][1]), i[0][0]))
        for i in right_targets:
            right_targets_real.append(VISION_TARGET.location3d_by_params(camera, np.sqrt(i[0][1][0] * i[0][1][1]), i[0][0]))

        vt_distance = 0.2866
        vector_distance = np.array([vt_distance / 2, 0, 0])

        all_hatches = []
        for i, t in enumerate(left_targets_real):
            if len(left_targets[i][1]) != 4:
                #print('[WARN] polydp returning %d points instead of four' % len(left_targets[i][1]))
                continue
            width, height = left_targets[i][0][1]
            tmp_ang = np.deg2rad(90.0 + left_targets[i][0][2])
            w_s = np.cos(tmp_ang) * width + np.sin(tmp_ang) * height
            h_s = np.sin(tmp_ang) * width + np.cos(tmp_ang) * height
            poly = np.array(left_targets[i][1])
            _ = sorted(poly, key=lambda p: p[1])
            highest = _[0]
            lowest = _[3]
            _ = sorted(poly, key=lambda p: p[0])
            leftest = _[0]
            rightest = _[3]
            sng = -np.sign(np.linalg.norm(leftest - lowest) - np.linalg.norm(rightest - highest))
            angle = sng*np.arccos(min(min(w_s / h_s, h_s / w_s) / ENCLOSING_RECT_MAX_RATIO, 1))
            rot_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                   [0, 1, 0],
                                   [-np.sin(angle), 0, np.cos(angle)]])
            all_hatches.append(t - rot_matrix.dot(vector_distance))

        for i, t in enumerate(right_targets_real):
            if len(right_targets[i][1]) != 4:
                #print('[WARN] polydp returning %d points instead of four' % len(right_targets[i][1]))
                continue
            width, height = right_targets[i][0][1]
            tmp_ang = np.deg2rad(abs(right_targets[i][0][2]))
            w_s = np.cos(tmp_ang) * width + np.sin(tmp_ang) * height
            h_s = np.sin(tmp_ang) * width + np.cos(tmp_ang) * height
            poly = np.array(right_targets[i][1])
            _ = sorted(poly, key=lambda p: p[1])
            highest = _[0]
            lowest = _[3]
            _ = sorted(poly, key=lambda p: p[0])
            leftest = _[0]
            rightest = _[3]
            sng = -np.sign(np.linalg.norm(leftest - highest) - np.linalg.norm(rightest - lowest))
            angle = sng*np.arccos(min(min(w_s / h_s, h_s / w_s) / ENCLOSING_RECT_MAX_RATIO, 1))
            rot_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                   [0, 1, 0],
                                   [-np.sin(angle), 0, np.cos(angle)]])
            all_hatches.append(t + rot_matrix.dot(vector_distance))

        cv2.imshow('feed', frame)

        k = cv2.waitKey(1) & 0xff

        if k == ord('d'):
            print(all_hatches[0] if len(all_hatches) > 0 else None)
            print(all_hatches[1] if len(all_hatches) > 1 else None)

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
