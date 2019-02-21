import cv2
import matplotlib.pyplot as plt
import numpy as np
from models import PORT

from genetic_threshold import find_optimized_parameters, prep_image


def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def main():
    src = []
    boxes = []
    video = cv2.VideoCapture(PORT)
    video.set(cv2.CAP_PROP_EXPOSURE, -6)
    src_path = raw_input("enter path to file (stop to exit): ")
    if src_path != "stop":
        src_fix_path = raw_input("enter path to fixed file: ")
    else:
        src_fix_path = ""  # suppress warning
    while src_path != "stop" and src_fix_path != "stop":
        src.append(cv2.imread(src_path))
        boxes.append(prep_image(cv2.imread(src_fix_path)))
        src_path = raw_input("enter path to file(stop to exit): ")
        if src_path != "stop":
            src_fix_path = raw_input("enter path to fixed file: ")
    params, scores = find_optimized_parameters(threshold, src, boxes, (3, 2),
                                               c_factor=5, alpha=5, survivors_size=20,
                                               gen_size=1000, gen_random=100, max_iter=15,
                                               range_regulator=np.array([0.1, 0.4, 0.4]))
    plt.plot(np.arange(len(scores)), scores)
    print(map(list, params.astype(int)))
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
