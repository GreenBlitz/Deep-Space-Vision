import cv2
import numpy as np
from tools.find_optimized_parameters import find_optimized_parameters
import matplotlib.pyplot as plt

def threshold(frame, params):
    """
    filters the colors by the range of RGB
    :param frame: is de video
    :param params: are d
    :return:
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def main():
    src = []
    boxes = []
    video = cv2.VideoCapture(1)
    while True:
        ok, frame = video.read()
        cv2.imshow('window', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('r'):
            bbox = cv2.selectROI('window', frame)
            boxes.append(bbox)
            src.append(frame)
        if k == ord('c'):
            cv2.destroyAllWindows()
            break
    params, scores = find_optimized_parameters(threshold, src, boxes, (3, 2), c_factor=5, alpha=5, survivors_size=10, gen_size=1000, gen_random=100, max_iter=20)
    plt.plot(np.arange(len(scores)), scores)
    print(params)
    plt.show()
    while True:
        cv2.imshow('original', src[0])
        cv2.imshow('threshold', threshold(src[0], params))
        if cv2.waitKey() & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break
    while True:
        ok, frame = video.read()
        cv2.imshow('threshold', threshold(frame, params))
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break
    import IPython
    IPython.embed()

if __name__ == '__main__':
    main()