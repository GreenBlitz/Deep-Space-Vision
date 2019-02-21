import cv2
import numpy as np


def corners(im):
    return cv2.filter2D(im, -1, np.array([[-1, 1], [1, -1]]))


def edges(im):
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]))


def sharpen(im):
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


def blur(im):
    return cv2.filter2D(im, -1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9)


def blue(im):
    return im[:, :, 0]


def green(im):
    return im[:, :, 1]


def red(im):
    return im[:, :, 2]


def gray(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


def crop(im, x, y, w, h):
    return im[y:y + h, x:x + w, :]
