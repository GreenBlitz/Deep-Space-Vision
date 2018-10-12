import cv2
import numpy as np
import functools

class PipeLine:
    def __init__(self, *functions):
        self.functions = list(functions)

    def __call__(self, image:np.ndarray):
        return functools.reduce(lambda x, f: f(x), self.functions, image)

    def __add__(self, other):
        return PipeLine(*self.functions + other.functions)

    def __iadd__(self, fun):
        self.functions += fun.functions

    def __getitem__(self, item):
        return self.functions[item]

    def __setitem__(self, key, value):
        self.functions[key] = value
