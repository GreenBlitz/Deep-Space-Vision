from models import *
from utils import *
from vision import *
from drawings import *
from funcs import *

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

        for i, c in enumerate(circles):
            cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), (0, 255, 0), 2)
            cv2.circle(frame, (int(c[0][0]), int(c[0][1])), 2, (0, 0, 255), 2)
            d = FUEL.location3d_by_params(camera, SQRT_PI*c[1], c[0])
            cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
            cv2.putText(frame, str((d*1000).astype(int).astype(float)/1000), (int(c[0][0]-75), int(c[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

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
