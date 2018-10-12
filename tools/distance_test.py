import cv2
import numpy as np
from tools.cameras import Camera
from tools.pipeline import PipeLine
from tools.conv_tools import blur

array = np.array

red_detection_params = [array([19.39925944, 45.96760714]), array([ 88.45797967, 191.11653479]), array([112.4847102 , 203.04345544])]

def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))




pipeline = PipeLine(lambda frame: threshold(frame, red_detection_params),
                    lambda frame: cv2.erode(frame, np.ones((3,3))),
                    lambda frame: cv2.dilate(frame, np.ones((3,3)), iterations=4))
                    #lambda frame: cv2.erode(frame, np.ones((3,3))))

pipeline1 = pipeline + PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1],
                    lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True),
                    lambda cnts: cnts[0] if len(cnts) > 0 else None)

pipeline2 = PipeLine(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)),
                    lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                    lambda polydp: map(lambda x: x[0], polydp),
                    lambda polydp: list(map(tuple, polydp)))

pipeline3 = PipeLine(lambda cnt: cv2.moments(cnt),
                     lambda m: (m['m10']/(m['m00'] + 0.000001), m['m01']/(m['m00'] + 0.000001)))

pipeline4 = pipeline + PipeLine(lambda frame: cv2.distanceTransform(frame, cv2.DIST_L2, 3))

def main():
    camera = Camera(1, 648.5256168410046)
    area = 0.22510163906500055/2
    theta = 0.340394
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', pipeline(frame))
        cnt = pipeline1(frame)



        if cnt is not None:
            pixel_area = np.sqrt(cv2.contourArea(cnt))
            polydp = pipeline2(cnt)
            cv2.drawContours(frame, [cnt], 0, (0, 255, 0) ,2)
            #for i, val in enumerate(polydp):
            #    cv2.line(frame, val, polydp[(i + 1) % len(polydp)], (255, 0, 0), 3)

            object_center = np.array(pipeline3(cnt))

            frame_center = np.array(frame.shape[:2][::-1])/2

            norm_d = area*camera.constant/(pixel_area + 0.00000001)

            vp = object_center - frame_center

            alpha = theta*vp[0]/frame_center[0]

            d = norm_d*np.array([np.sin(alpha), np.cos(alpha)])


        cv2.imshow('original', frame)
        #cv2.imshow('pipe', thr)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('d'):
            print(d)
            print(norm_d)

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
