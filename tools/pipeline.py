import cv2
import numpy as np

class PipeLine:
    def __init__(self, *functions):
        self.functions = list(functions)

    def __call__(self, image:np.ndarray):
        for i in self.functions:
            image = i(image)
        return image

    def __add__(self, other):
        return PipeLine(self, other)

    def __iadd__(self, fun):
        self.functions.append(fun)


