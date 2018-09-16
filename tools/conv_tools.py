import numpy as np

def convolve(src:np.ndarray, kernel:np.ndarray):
    assert len(kernel.shape) == len(src.shape)

    if len(kernel.shape) == 1:
        return np.convolve(src, kernel)

    return_mat = []

    for i in range(len(src)-len(kernel)):
        mat = src[(kernel.shape[0] + i,) + kernel.shape[1:]]
        for j, m_src in enumerate(mat):
            return_mat.append(convolve(m_src, kernel[j]))
    return np.array(return_mat)