import numpy as np

def convolve(src:np.ndarray, kernel:np.ndarray) -> np.ndarray:
    assert len(kernel.shape) == len(src.shape)

    if len(kernel.shape) == 1:
        return np.convolve(src, kernel)

    return __convolve(src, kernel, [])

def subtensor(src:np.ndarray, start_ind:list, end_ind:list or np.ndarray, index=0) -> np.ndarray:
    if len(src.shape) == 1:
        return src[start_ind[index]:end_ind[index]]
    return_arr = []
    for i in range(start_ind[index], end_ind[index]):
        return_arr.append(subtensor(src[i], start_ind, end_ind, index+1))
    return np.array(return_arr)

def __convolve(src:np.ndarray, kernel:np.ndarray, ind:list) -> np.ndarray:
    ax = len(ind)
    if ax == len(kernel.shape):
        return np.sum(subtensor(src, ind, np.array(ind) + np.array(kernel.shape))*kernel)
    return_arr = []
    for i in range(src.shape[ax] - kernel.shape[ax]):
        return_arr.append(__convolve(src, kernel, ind + [i]))
    return np.array(return_arr)
