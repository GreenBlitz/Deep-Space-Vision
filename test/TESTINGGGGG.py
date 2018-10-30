from models import *
from utils import *
from vision import *
from collections import deque


def is_rect_colliding(r1, r2):
    return not( (r1[0] + r1[2] < r2[0]) or (r2[0] + r2[2] < r1[0])  or (r1[1] + r1[3] < r2[1]) or (r2[1] + r2[3] < r1[1]) )


def find_ball_vel():
    camera = Camera(0, LIFECAM_STUDIO)
    ball_locs = deque()
    while True:
        ok, frame = camera.read()
        fuels = find_fuels(frame, camera)
        if len(ball_locs) > 0:
            ball_locs.append(fuels[0])
            if ball_locs.__len__() > 2:
                ball_locs.popleft()
            if ball_locs.__len__() == 2:
                ball_v = ball_locs[0][1]

        else:
            #fk this shit
            pass




def main():

    camera = Camera(0, LIFECAM_STUDIO)
    rtag = np.array([0, 0, 0, 0])
    while True:
        ok, frame = camera.read()
        thr = threshold_trash(frame)
        cv2.imshow('hello i is vision', thr)
        d = 0
        cnts = sorted_contours(thr)
        rects = contours_to_rects_sorted(cnts)

        if len(rects) > 0:
            if rects[0][2]*rects[0][3] < rtag[3]*rtag[2]:
                rtag = 0.8*rtag + 0.2*np.array(rects[0])
                rects[0] = tuple(list(rtag.astype(int)))
            else:
                rtag = np.array(rects[0])
        else:
            rects.append(tuple(list(rtag.astype(int))))
        d = TRASH.distance_by_params(camera, 0.8*np.sqrt(rects[0][2]*rects[0][3]))
        cv2.rectangle(frame, rects[0][:2], (rects[0][0]+rects[0][2], rects[0][1]+rects[0][3]), (0, 255, 0), 2)

        cv2.imshow('hello i is also vision', frame)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('d'):
            print d

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()