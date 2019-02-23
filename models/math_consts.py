import numpy as np

SQRT_PI = np.sqrt(np.pi)

CAMERA_ANGLE = -np.pi/3

CAMERA_ROTATION_MATRIX = np.array([[1, 0, 0],
                                   [0, np.cos(CAMERA_ANGLE), -np.sin(CAMERA_ANGLE)],
                                   [0, np.sin(CAMERA_ANGLE), np.cos(CAMERA_ANGLE)]])
