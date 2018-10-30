from models import *
from utils import *
from vision import *
from drawings import *

def main():

    camera = Camera(0, LIFECAM_STUDIO)
    time = 0
    while True:
        time += 1
        ok, frame = camera.read()
        thr = threshold_fuel(frame)
        cv2.imshow('hello i is vision', thr)
        d = []
        circles = find_fuel_circles(frame)
        cnts = fuel_contours_filtered(frame)

        for i, c in enumerate(circles):
            draw_flow(frame, cnts[i])
            cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), (0, 255, 0), 2)
            cv2.circle(frame, (int(c[0][0]), int(c[0][1])), 2, (0, 0, 255), 2)
            d.append(FUEL.location3d(camera=camera,
                                     pipeline=fuel_contours_filtered + (lambda x: x[0] if len(x) else None),
                                     frame=frame))

        cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 2, (255, 0, 0), 2)

        cv2.imshow('hello i is also vision', frame)

        k = cv2.waitKey(1) & 0xFF

        if time % 60 == 0 or k == ord('d') :
            print d

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
