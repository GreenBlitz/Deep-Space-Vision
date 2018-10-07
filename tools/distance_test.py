import cv2
import numpy as np
from tools.cameras import Camera
from tools.pipeline import PipeLine

red_detection_params =  np.array([[173.46106735, 188.03026678],
                                  [ 66.49687872, 142.5853625 ],
                                  [133.48859651, 189.53074141]])

def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))




pipeline = PipeLine(lambda frame: threshold(frame, red_detection_params))

pipeline1 = pipeline + PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1],
                    lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True),
                    lambda cnts: cnts[0] if len(cnts) > 0 else None)

pipeline2 = PipeLine(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)),
                    lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                    lambda polydp: map(lambda x: x[0], polydp),
                    lambda polydp: list(map(tuple, polydp)))

def main():
    camera = Camera(1, 648.5256168410046)
    while True:
        ok, frame = camera.read()
        cv2.imshow('ooooo', pipeline(frame))
        cnt = pipeline1(frame)
        if cnt is not None:
            pixel_area = np.sqrt(cv2.contourArea(cnt))
            polydp = pipeline2(cnt)
            for i, val in enumerate(polydp):
                cv2.line(frame, val, polydp[(i + 1) % len(polydp)], (255, 0, 0), 10)

            polydp = np.array(polydp)

            area = 0.146

            object_center = polydp.mean(axis=0)

            frame_center = np.array(frame.shape[:2])/2

            norm_d = area*camera.constant/(pixel_area + 0.00000001)

            vp = object_center - frame_center

            d = vp*norm_d/(np.linalg.norm(vp) + 0.00000001)

            print(d)
            print(norm_d)

        cv2.imshow('original', frame)
        #cv2.imshow('pipe', thr)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


def measure_distance(camera, area):
    area = np.sqrt(area)
    ok, frame = camera.read()
    cv2.imshow('ooooo', pipeline(frame))
    cnt = pipeline1(frame)
    if cnt is not None:
        pixel_area = np.sqrt(cv2.contourArea(cnt))
        polydp = pipeline2(cnt)

        polydp = np.array(polydp)

        object_center = polydp.mean(axis=0)

        frame_center = np.array(frame.shape[:2]) / 2

        norm_d = area * camera.constant / (pixel_area + 0.00000001)

        vp = object_center - frame_center

        d = vp * norm_d / (np.linalg.norm(vp) + 0.00000001)

        return d

    return None


if __name__ == '__main__':
    main()
