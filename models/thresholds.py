import cv2


def hls_threshold(frame, params):
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


def hsv_threshold(frame, params):
    """
    thresholds the image according to HSV values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def rgb_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


THRESHOLD_NAME_TABLE = {
    'RGB': rgb_threshold,
    'HLS': hls_threshold,
    'HSV': hsv_threshold
}


#FUEL_THRESHOLD = [[19.39925944, 45.96760714], [ 88.45797967, 191.11653479], [112.4847102 , 203.04345544]]
#FUEL_THRESHOLD = [[33.27126693, 47.31689005], [110.49726198, 148.57312153], [139.49983957, 168.50129412]]

class Threshold:
    def __init__(self, lst, thresh_type='HSV'):
        assert thresh_type in THRESHOLD_NAME_TABLE
        self.init = lst
        self.type = thresh_type.upper()

    def __len__(self):
        return len(self.init)

    def __getitem__(self, item):
        return self.init[item]

    def __setitem__(self, key, value):
        self.init[key] = value

    def __iter__(self):
        return iter(self.init)

    def __call__(self, frame):
        return THRESHOLD_NAME_TABLE[self.type](frame, self.init)


FUEL_THRESHOLD = Threshold(
    [[33.46342507, 45.14846628], [90.4936124, 182.02390718], [129.49086936, 194.548855]],
    'HLS'
)
