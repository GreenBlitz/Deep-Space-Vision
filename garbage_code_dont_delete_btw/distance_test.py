import cv2
import numpy as np
from cameras import Camera
from pipeline import PipeLine
from image_objects import ImageObject
array = np.array


def crop_image(img, x, y, w, h):
    return img[y:y+h, x:x+w, :]


def is_circle_invalid(center1, r1, center2, r2):
    """
    checks for BallCeption
    :param center1:
    :param r1:
    :param center2:
    :param r2:
    :return:
    """
    return (center1[0] - center2[0])**2 + (center1[1] - center2[1])**2 < (r1+r2)**2

def p_ball(carea, r):
    return carea/(2*np.pi*(r**2))

"""
HLS threshold for fuel (the annoying little yellow ballz) 
"""
#red_detection_params = [array([19.39925944, 45.96760714]), array([ 88.45797967, 191.11653479]), array([112.4847102 , 203.04345544])]
#red_detection_params = [array([33.27126693, 47.31689005]), array([110.49726198, 148.57312153]), array([139.49983957, 168.50129412])]
red_detection_params = [array([33.46342507, 45.14846628]), array([ 90.4936124 , 182.02390718]), array([129.49086936, 194.548855  ])]


def threshold(frame, params):
    """
    thresholds the image according to HLS values
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
                    lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True))

"""
pipeline from image to contours of fuel (balls)
"""

pipeline_cnts = pipeline + PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1],
                                    lambda cnts: filter(lambda c: cv2.contourArea(c) >= 300.0, cnts),
                                    lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True))

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


def detect_balls_by_radius():
    """
    get coordinates and distance of all balls
    """
    camera = Camera(0, 648.5256168410046, 0.340394)
    ball = ImageObject(0.22510163906500055 / 2)
    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', pipeline(frame))
        cnts = list(pipeline_cnts(frame))
        d = []
        d_norm = []
        rs = []
        centers = []
        if len(cnts) > 0:
            for cnt in cnts:
                to_continue = False
                center, r = cv2.minEnclosingCircle(cnt)
                #if p_ball(cv2.contourArea(cnt), r) # 0.0:
                #    continue
                for i in range(len(rs)):
                    if is_circle_invalid(center1=center, r1=r, center2=centers[i], r2=rs[i]):
                        to_continue = True
                        break

                if to_continue:
                    continue

                centers.append(center)
                rs.append(r)
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


balls_count = 0
non_balls_count = 0

class ImageOfObject:
    def __init__(self, image, c, r):
        self.images = [image]
        self.center = c
        self.r = r
        self.counter = 30
        self.label = "not_a_ball"
        self.was_found = False

    def copy(self, img, c, r):
        self.images.append(img)
        self.center = c
        self.r = r
        self.counter -= 1
        self.was_found = True
        if self.counter <= 0:
            self.label = "ball"
            self.save()

    def save(self):
        for i in self.images:
            if i.size == 0:
                continue
            path = './' + self.label + "/" + self.label + str(balls_count if self.label == "ball" else non_balls_count) + ".bmp"
            if self.label == 'ball':
                globals()['balls_count'] += 1
            else:
                globals()['non_balls_count'] += 1
            cv2.imwrite(path, cv2.resize(i, (32, 32)))
        self.images = []

def find_ball_in_list(c, r, l, img):
    for i in l:
        if np.linalg.norm(c - i.center) <= 0.1*i.r and abs(i.r - r) <= 0.1*i.r:
            i.copy(img, c, r)
            return True
    return False


def get_labeled_ball_images():
    """
    get coordinates and distance of all balls
    """
    camera = Camera(0, 648.5256168410046, 0.340394)
    ball = ImageObject(0.22510163906500055 / 2)

    images = []

    while True:
        ok, frame = camera.read()
        cv2.imshow('feed', pipeline(frame))
        cnts = list(pipeline_cnts(frame))
        rs = []
        centers = []
        new_images = []
        for i in images:
            i.was_found = False
        if len(cnts) > 0:
            for cnt in cnts:
                to_continue = False
                center, r = cv2.minEnclosingCircle(cnt)
                center = np.array(center, dtype=int)
                r = int(r)
                b_img = np.copy(frame[center[1] - r:center[1] + r, center[0] - r:center[0] + r, :])

                for i in range(len(rs)):
                    if is_circle_invalid(center1=center, r1=r, center2=centers[i], r2=rs[i]):
                        to_continue = True
                        break

                if to_continue:
                    continue

                if not find_ball_in_list(center, r, images, b_img):
                    new_images.append(ImageOfObject(b_img, center, r))

                rs.append(r)
                centers.append(center)
        images.extend(new_images)
        for i, img in enumerate(images):
            if not img.was_found:
                img.save()
                del images[i]
        for ind, center in enumerate(centers):
            cv2.circle(frame, tuple(map(int, center)), int(rs[ind]), (0, 255, 0), 2)
            cv2.circle(frame, tuple(map(int, center)), 2, (0, 0, 255), 2)
        cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 2, (255, 0, 0), 2)
        cv2.imshow('original', frame)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    detect_balls_by_radius()

