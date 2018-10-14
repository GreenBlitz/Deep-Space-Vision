import cv2
import numpy as np
from genetic_algorithm_v2 import find_optimized_parameters, prep_image
import matplotlib.pyplot as plt


def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def nuky_test(image_generator):
    """
    the test that nuky wanted
    :param image_generator: a generator of image/threshold image pairs
    :return: the original image/threshold image, the output parameters and the threshold image (yields)
    """
    for img, black_img in image_generator:
        b_img = prep_image(black_img)
        params, scores = find_optimized_parameters(threshold, [img], [b_img], (3, 2), c_factor=5, alpha=5,
                                                   survivors_size=10, gen_size=1000, gen_random=100, max_iter=20,
                                                   range_regulator=0.5)
        yield img, black_img, params, threshold(img, params)


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
            ft = np.zeros(frame.shape[:-1])
            ft[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]] = 1
            s = ft.mean()
            ft = np.vectorize(lambda x: -1 if x == 0 else (1-s)/s)(ft)
            #print(np.sum(ft))
            boxes.append(ft)
            src.append(frame)
        if k == ord('c'):
            cv2.destroyAllWindows()
            break
    params, scores = find_optimized_parameters(threshold, src, boxes, (3, 2),
                                               c_factor=5, alpha=5, survivors_size=20,
                                               gen_size=1000, gen_random=100, max_iter=15,
                                               range_regulator=np.array([0.1, 0.5, 0.5]))
    plt.plot(np.arange(len(scores)), scores)
    print(list(params))
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
    exit()

    im, thr = cv2.imread('img0.bmp'), cv2.imread('img0thr.bmp')
    while cv2.waitKey(1) & 0xff != ord('c'):
        cv2.imshow('f', thr)
    thr = prep_image(thr)

    while cv2.waitKey(1) & 0xff != ord('c'):
        cv2.imshow('f', thr)

    cv2.destroyAllWindows()

    params, scores = find_optimized_parameters(threshold, [im], [thr], (3, 2),
                                               c_factor=5, alpha=5, survivors_size=20,
                                               gen_size=1000, gen_random=100, max_iter=15,
                                               range_regulator=np.array([0.05, 0.1, 0.1]))
    plt.plot(np.arange(len(scores)), scores)
    print(list(params))
    plt.show()


    #v = cv2.VideoCapture(1)
    #index = 0
    #while True:
    #    _, frame = v.read()
    #    cv2.imshow('hello', frame)
    #    k = cv2.waitKey(1) & 0xFF
#
    #    if k == ord('r'):
    #        cv2.imwrite('img%i.bmp'%index, frame)
    #        index += 1
    #    if k == ord('c'):
    #        cv2.destroyAllWindows()
    #        break
#
    #main()