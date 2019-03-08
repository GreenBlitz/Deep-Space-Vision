from utils import *
from models import *
import tools.find_threshold

def make_frame_with_circle(frame, circ, thicknss=-1):
    ret = frame * 0
    cv2.circle(ret, (int(circ[0][0]), int(circ[0][1])), int(circ[1]), color=(255, 255, 255),
               thickness=thicknss)
    print(type(ret), "ret")
    return ret


def this_threshold(frame, params):
    genetic_thr = Threshold(params, 'HSV')(frame)
    thr = (threshold_cargo + find_contours + contours_to_circles + PipeLine(lambda circs: frame * 0 if len(circs) == 0 else sum(map(lambda circ: make_frame_with_circle(frame, circ), circs))))(frame)
    print(type(thr), "thr")
    print(type(genetic_thr), "gthr")

    zipped_rows = list(zip(thr, genetic_thr))
    zipped_pic = map(lambda tupled_row: list(zip(tupled_row[0], tupled_row[1])), zipped_rows)
    return list(map(lambda zipped_row: list(map(lambda tupled_pix: (255, 255, 255) if (tupled_pix[0][0] == tupled_pix[1][0] == 255) else (0, 0, 0), zipped_row)), zipped_pic))


def main():
    camera = Camera(0, LIFECAM_3000)
    params = ([4, 33], [36, 126], [121, 255])

    camera.set_exposure(-4)

    find_and_filter = find_contours + (
        lambda cnts: filter(lambda x: len(x) >= 5, cnts)) + filter_contours + sort_contours
    while True:
        ok, frame = camera.read()
        cv2.waitKey(1)
        while not ok:
            ok, frame = camera.read()
            print(ok)
        thr = this_threshold(frame, params)
        print(type(thr), "thrNow")
        cnts = (find_and_filter + sort_contours)(thr)
        circs = (contours_to_circles + filter_inner_circles)(cnts)
        #cnts_and_circs = (lambda x: filter_inner_circles   zip(cnts , circs)

        elps = contours_to_ellipses(cnts)
        # print([len(circs), len(elps), "bla"])
        num_of_cargos = [None] * len(circs)
        num_of_cargos2 = [None] * len(circs)

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

        for i in range(len(circs)):
            # print(i, "bla2")
            circ = circs[i]
            elp = elps[i]
            cnt = cnts[i]
            # print(elp)
            # print(circ)
            cv2.ellipse(frame, elp,
                        color=colors[i % len(colors)], thickness=5)
            cv2.circle(frame, (int(circ[0][0]), int(circ[0][1])), int(circ[1]), color=colors[i % len(colors)],
                       thickness=5)
            areas_porsion = 2.5 * circ[1] * circ[1] / (elp[1][0] * elp[1][1])
            areas_porsion2 = np.pi * circ[1] * circ[1] / cv2.contourArea(cnt)
            num_of_cargos[i] = max(np.round(areas_porsion), 1)
            num_of_cargos2[i] = max(np.round(areas_porsion2), 1)

        cv2.imshow("feed", frame)
        cv2.imshow("threshold", thr)
        #print(num_of_cargos)
        print(sum(num_of_cargos))
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
