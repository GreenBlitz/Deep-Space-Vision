from models import *
from utils import *
from utils.net import *



def main():
    camera = Camera(PORT, LIFECAM_3000)
    camera.set_exposure(-13)
    conn = net_init()


    while True:
        ok, frame = camera.read()
        vts = (threshold_vision_target + find_contours + filter_contours + sort_contours)(frame)
        vt_r = list(find_vision_target(frame, camera))
        aad = []
        for i, vt in enumerate(vts):
            cv2.drawContours(frame, [vt], 0, (0, 0, 255), 5)
            c = [contour_center(vt)]
            d = vt_r[i]
            cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 4)
            cv2.putText(frame, str((d * 1000).astype(int).astype(float) / 1000), (int(c[0][0] - 75), int(c[0][1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            aad.append(np.linalg.norm(vt_r[i]))
            if i == 1:
                a = np.array(vt_r[0])
                b = np.array(vt_r[1])
                center = (a + b)/2
                dis = np.linalg.norm(center)
                ang = np.rad2deg(np.arctan(center[0]/ center[2]))
                conn.set('hatch::distance', dis)
                conn.set('hatch::ang', ang)
                print("angle: %s" % ang)
               # print("distance: %s" % dis)
                break


        cv2.imshow('feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
