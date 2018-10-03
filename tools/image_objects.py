import numpy as np
import cv2
from tools.cameras import Camera


class ImageObject:
    def __init__(self, dimensions):
        self.dimensions = dimensions