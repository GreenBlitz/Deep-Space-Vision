from models import *
from utils import *


def main():
    camera = Camera(1, LIFECAM_STUDIO)
    import os
    os.system('v4lt-clt -d /dev/video0 -c exposure_auto=1')
    os.system('v4lt-ctl -d /dev/video0 -c exposure_auto=6')
    #print(camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera.get(cv2.CAP_PROP_FRAME_WIDTH)//4))
    #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera.get(cv2.CAP_PROP_FRAME_HEIGHT)//4)
    camera.data.constant /= 4

    time = 0
    #camera.toggle_auto_exposure(1)
    #camera.set_exposure(-6)
    while True:
        time += 1
        ok, frame = camera.read()
        thr = threshold_cargo(frame)
        print(cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1])
        cv2.imshow('Hello I is vision', thr)
        d = []
        try:
            circles = (
                    threshold_cargo + find_contours + filter_contours + sort_contours + contours_to_circles_sorted + filter_inner_circles)(
                frame)

            circles = circles[:1]
            for i, c in enumerate(circles):
                cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), (0, 255, 0), 2)
                cv2.circle(frame, (int(c[0][0]), int(c[0][1])), 2, (0, 0, 255), 2)
                d = CARGO.location3d_by_params(camera, SQRT_PI * c[1], c[0])
                # cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
                # cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
                cv2.putText(frame, str(int(np.linalg.norm(d)*1000)/1000.0), (int(c[0][0]), int(c[0][1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
                cv2.putText(frame, str(int(np.linalg.norm(d)*1000)/1000.0), (int(c[0][0]), int(c[0][1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

            cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 2, (255, 0, 0), 2)
        except:pass

        cv2.imshow('hello i is also vision', frame)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('d'):
            print(d)
            print(np.linalg.norm(d))

        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
