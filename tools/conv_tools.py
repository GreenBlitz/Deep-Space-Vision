import numpy as np
import cv2

def _relu(x):
    return 0 if x<0 else x

def _pixelize(x):
    return int(min(max(x, 0), 255))

relu = np.vectorize(_relu)

pixelize = np.vectorize(_pixelize)



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
    for i in range(src.shape[ax] - kernel.shape[ax]+1):
        return_arr.append(__convolve(src, kernel, ind + [i]))
    return np.array(return_arr)

def main():
    im = cv2.imread(r"C:\Users\HEINEMANN\Downloads\some.jpeg")

    c = sharpen(im)
    while True:
        cv2.imshow('grayscale', c)
        if cv2.waitKey(0) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


def edges(im:np.ndarray) -> np.ndarray:
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]))

def sharpen(im:np.ndarray) -> np.ndarray:
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


if __name__ == '__main__':
    main()