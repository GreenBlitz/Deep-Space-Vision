from models import *
from utils import *


def main():
    camera = Camera(PORT, MICROSOFT_CAM)
    camera.set_exposure(-13)

    while True:
        ok, frame = camera.read()
        vts = (threshold_vision_target + find_contours + sort_contours + filter_contours)(frame)
        vt_r = find_vision_target(frame, camera)
        aad = []
        for i, vt in enumerate(vts):
            cv2.drawContours(frame, [vt], 0, (255, 0, 0), 5)
            c = [contour_center(vt)]
            d = vt_r[i]
            cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
            cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            aad.append(np.linalg.norm(vt_r[i]))

        print(aad)
        cv2.imshow('feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
