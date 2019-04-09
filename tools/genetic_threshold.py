import random

import cv2
import numpy as np


def prep_image(img):
    if len(img.shape) == 3:
        f = cv2.inRange(img, (1, 0, 0), (255, 255, 255))
        f = cv2.bitwise_or(f, cv2.inRange(img, (0, 1, 0), (255, 255, 255)))
        f = cv2.bitwise_or(f, cv2.inRange(img, (0, 0, 1), (255, 255, 255)))
    else:
        f = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
    s = f.mean() / 255.0
    return np.vectorize(lambda x: (-1.0) if x == 0 else ((1.0 - s) / s))(f.astype(float))


def create_params(shape, factor):
    return np.random.rand(*shape) * factor


def get_score(item, frame, bbox, func, reg):
    frametag = func(frame, item)
    return np.mean(frametag * bbox) - (reg * np.abs(item[:, 0] - item[:, 1])).sum()


def create_child(sur, alpha, factor):
    child = np.sign(np.random.rand(*sur[0].shape) - 0.5) * 10 ** (-alpha * np.random.rand(*sur[0].shape)) * factor
    for i in range(len(sur[0])):
        child[i] += random.choice(sur)[i]
    return child


def find_optimized_parameters(func, images, bboxes, p_shape, gen_size=1000,
                              survivors_size=20, p_factor=255, alpha=50, max_iter=10,
                              gen_random=5, c_factor=1, range_regulator=0.5):
    gen = []
    all_scores = []
    best = None
    max_score = -np.inf
    for i in range(gen_size):
        gen.append(create_params(p_shape, p_factor))
    for _ in range(max_iter):
        scores = []
        all_scores.append(0)
        for i in gen:
            sum = 0
            for j, im in enumerate(images):
                sum += get_score(i, im, bboxes[j], func, range_regulator)
            scores.append([i, sum])
            all_scores[_] = max(all_scores[_], sum)
            if sum > max_score:
                max_score = sum
                best = i

        survivors = list(map(lambda x: x[0].flatten(), sorted(scores, key=lambda x: x[1], reverse=True)))[
                    :survivors_size]
        gen = []
        for i in range(gen_size - gen_random):
            gen.append(create_child(survivors, alpha, c_factor).reshape(p_shape))
        for i in range(gen_random):
            gen.append(create_params(shape=p_shape, factor=p_factor))
    return best, all_scores
