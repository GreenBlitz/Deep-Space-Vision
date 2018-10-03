import cv2
import random
import numpy as np

def create_params(shape:tuple, factor:float or int or np.ndarray=1) -> np.ndarray:
    '''
    the best function ever - Top 10
    :param shape: de ting goes skraaa, the type of parameter
    :param factor: the factor in which the changenings happpen
    :return:
    '''
    return np.random.rand(*shape)*factor

def get_score(item:np.ndarray, frame:np.ndarray, bbox:tuple, func, reg):
    """
    returns the fitness value the sperm
    :param item: sperm
    :param frame: da way of de camera
    :param bbox: threasholdeded squerere
    :param func: LosGreengos-Threasholdos tm
    :param reg: regulater number or matrix for range control,(prevents autisem)
    :return:
    """
    frametag = func(frame, item)
    f = frametag[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
    s = f.sum()
    return s/f.size - (frametag.sum() - s)/(frametag.size - f.size) - reg*(np.abs(item[:,0] - item[:,1]).sum())

def create_child(sur, alpha, factor):
    '''
    when the father and the mother love each other very much...
    *** the function may take up to nine months
    :param sur:
    :param alpha:
    :param factor:
    :return:
    '''
    child = np.sign(np.random.rand(*sur[0].shape))* 10**(-alpha * np.random.rand(*sur[0].shape))*factor
    for i in range(len(sur[0])):
        child[i] += random.choice(sur)[i]
    return child


def find_optimized_parameters(function, images, bboxes, p_shape, gen_size=50, survivors_size=0, p_factor=255, alpha=50, max_iter=100, gen_random=5, c_factor=1, s_reg=0.5):
    """
    fucking the hell out of stupid children and keeping only the ones without autisem
    :param function:
    :param images:
    :param bboxes:
    :param p_shape:
    :param gen_size:
    :param survivors_size:
    :param p_factor:
    :param alpha:
    :param max_iter:
    :param gen_random:
    :param c_factor:
    :param s_reg:
    :return:
    """
    gen = []
    scores = []
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
                sum += get_score(i, im, bboxes[j], function, s_reg)
            scores.append([i, sum])
            all_scores[_] = max(all_scores[_], sum)
            if sum > max_score:
                max_score = sum
                best = i

        survivors = list(map(lambda x: x[0].flatten(), sorted(scores, key=lambda x: x[1], reverse=True)))[:survivors_size]
        gen.clear()
        for i in range(gen_size-gen_random):
            gen.append(create_child(survivors, alpha, c_factor).reshape(p_shape))
        for i in range(gen_random):
            gen.append(create_params(shape=p_shape, factor=p_factor))
    return best, all_scores

