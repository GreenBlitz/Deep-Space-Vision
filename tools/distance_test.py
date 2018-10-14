import cv2
import numpy as np
from tools.cameras import Camera
from tools.pipeline import PipeLine
from tools.image_objects import ImageObject
array = np.array

"""
hls threshold for fuel (the annoying little yellow balls) 
"""
red_detection_params = [array([19.39925944, 45.96760714]), array([ 88.45797967, 191.11653479]), array([112.4847102 , 203.04345544])]

def threshold(frame, params):
    """
    thresholds the image according to hls values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


"""
pipeline from image to binary image of the fuel (annoying little yellow balls)
"""
pipeline = PipeLine(lambda frame: threshold(frame, red_detection_params),
                    lambda frame: cv2.erode(frame, np.ones((3,3))),
                    lambda frame: cv2.dilate(frame, np.ones((3,3)), iterations=4))

"""
pipeline from image to contour of largest (closest) fuel (ball)
"""
pipeline1 = pipeline + PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1],
                    lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True),
                    lambda cnts: cnts[0] if len(cnts) > 0 else None)

"""
pipeline from image to contours of fuel (balls)
"""
pipeline_cnts = pipeline + PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1],
                    lambda cnts: filter(lambda c: cv2.contourArea(c) >= 300.0, cnts))

"""
pipeline from a single contour to polygon representation
"""
pipeline2 = PipeLine(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)),
                    lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                    lambda polydp: map(lambda x: x[0], polydp),
                    lambda polydp: list(map(tuple, polydp)))

"""
pipeline from a single contour to it's center x,y coordinates
"""
pipeline3 = PipeLine(lambda cnt: cv2.moments(cnt),
                     lambda m: (int(m['m10']/(m['m00'] + 0.0000001)), int(m['m01']/(m['m00'] + 0.0000001))))

"""
pipeline from image to the area in pixels of the largest fuel (closest ball) seen in the image
"""
pipeline4 = pipeline1 + PipeLine(lambda cnt: np.sqrt(cv2.contourArea(cnt)))

def main():
    """
    get coordinates and distance of a single ball (closest)
    """
    camera = Camera(1, 648.5256168410046, 0.340394)
    ball = ImageObject(0.22510163906500055/2)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', pipeline(frame))
        cnt = pipeline1(frame)

        if cnt is not None:
            cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2)
            c = pipeline3(cnt)
            cv2.circle(frame, c, 2, (0,0,255),2)
            cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 2, (255,0,0),2)

        cv2.imshow('original', frame)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('d'):
            print(ball.location2d(camera, pipeline1, frame))
            print(ball.distance(camera, pipeline4, frame))

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


def main2():
    """
    get coordinates and distance of all balls
    """
    camera = Camera(1, 648.5256168410046, 0.340394)
    ball = ImageObject(0.22510163906500055 / 2)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', pipeline(frame))
        cnts = list(pipeline_cnts(frame))
        d = []
        d_norm = []
        if len(cnts) > 0:
            for cnt in cnts:
                c = pipeline3(cnt)
                cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2)
                cv2.circle(frame, c, 2, (0, 0, 255), 2)
                d.append(ball.location2d_by_contours(camera, cnt))
                d_norm.append(ball.distance_by_contours(camera, cnt))

            cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 2, (255, 0, 0), 2)


        cv2.imshow('original', frame)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('d'):
            print(d)
            print(d_norm)

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


def main3():
    """
    get coordinates and distance of all balls
    """
    camera = Camera(1, 648.5256168410046, 0.340394)
    ball = ImageObject(0.22510163906500055 / 2)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', pipeline(frame))
        cnts = list(pipeline_cnts(frame))
        d = []
        d_norm = []
        if len(cnts) > 0:
            for cnt in cnts:
                center, r = cv2.minEnclosingCircle(cnt)
                cv2.circle(frame, tuple(map(int, center)), int(r), (0, 255, 0), 2)
                cv2.circle(frame, tuple(map(int, center)), 2, (0, 0, 255), 2)
                area = np.sqrt(np.pi)*r
                d_norm.append(ball.distance_by_params(camera, area))
                d.append(ball.location2d_by_params(camera, area, center))


            cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 2, (255, 0, 0), 2)


        cv2.imshow('original', frame)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('d'):
            print(d)
            print(d_norm)

        if k == ord('c'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main3()

