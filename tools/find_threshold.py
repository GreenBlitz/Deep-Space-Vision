import matplotlib.pyplot as plt
from models import *
from utils import *

from tools.genetic_threshold import find_optimized_parameters


def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def main():
    src = []
    boxes = []
    video = Camera(PORT, None)
    video.set_exposure(-6)
    while True:
        ok, frame = video.read()
        cv2.imshow('window', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('r'):
            bbox = cv2.selectROI('window', frame)
            ft = np.zeros(frame.shape[:-1])
            ft[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]] = 1
            s = ft.mean()
            ft = np.vectorize(lambda x: -1 if x == 0 else (1 - s) / s)(ft)
            boxes.append(ft)
            src.append(frame)
        if k == ord('c'):
            cv2.destroyAllWindows()
            break
    params, scores = find_optimized_parameters(threshold, src, boxes, (3, 2),
                                               c_factor=5, alpha=5, survivors_size=20,
                                               gen_size=1000, gen_random=100, max_iter=10,
                                               range_regulator=np.array([0.02, 0.1, 0.1]))
    plt.plot(np.arange(len(scores)), scores)
    print(list(map(list, params.astype(int))))
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


if __name__ == '__main__':
    main()
