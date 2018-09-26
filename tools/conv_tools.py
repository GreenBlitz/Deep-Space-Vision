import numpy as np
import cv2
import time

def _relu(x):
    return 0 if x<0 else x

def _pixelize(x):
    return int(0 if x < 0 else 255 if x > 255 else x)

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


def find_red_square(im:np.ndarray, threshhold=100):
    im = im/(np.sum(im, axis=2) + 0.000001).reshape(im.shape[0:2] + (1,))*255

    im2 = red(im) - (green(im)+blue(im))*0.6
    im2 = relu(im2).astype('uint8')
    #blur = cv2.GaussianBlur(im2, (5, 5), 0)
    thr = (cv2.threshold(im2, threshhold, 255, cv2.THRESH_BINARY)[1])
    im2, contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None# [[0,0]]
    #contours = [i[0] for i in contours]
    #contours = [i.mean(axis=0) for i in contours]
    cv2.imshow('fuck', thr)
    return contours


    #cv2.drawContours(im, contours, 3, (0, 255, 0), 3)
    #ed = corners(thr)
    #ed = cv2.GaussianBlur(ed, (5, 5), 0)
    #return ed
    #ed = cv2.threshold(ed, 60, 255, cv2.THRESH_BINARY)[1]
    #im2, contours, hierarchy = cv2.findContours(ed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][1]
    #cv2.drawContours(im, contours, 3, (mov255,0), 3)
    #return ed






def main():
    from copy import deepcopy
    from datetime import datetime


    #arr = list(np.random.random_integers(0, 1000000000, 1000000))
    #arr1 = deepcopy(arr)

    #t0 = datetime.now()
    #print(bsort(arr))
    #tm = datetime.now()
    #print(qsort(arr1))
    #te = datetime.now()
    #print("Ido: " + str(tm - t0))
    #print("Alexey: " + str(te - tm))


    video = cv2.VideoCapture(1)  # set this to the path to the video file

    # Exit if video not opened.
    if not video.isOpened():
        raise Exception('error occured in opening video')

    # Read first frame

    ok, frame = video.read()

    a = np.array(find_red_square(frame))
    #x = a[:, 0]
    #y = a[:, 1]
    #x0, x1 = int(np.amin(x)), int(np.amax(x))
    #xy0 = int(x[np.argmin(y)])
    #xy1 = int(x[np.argmax(y)])
    #y0, y1 = int(np.amin(y)), int(np.amax(y))
    #yx0 = int(y[np.argmin(x)])
    #yx1 = int(y[np.argmax(x)])

    while True:
            # Read a new frame
            ok, frame = video.read()
            a = np.array(find_red_square(frame,100))
            #x = a[:,0]
            #y = a[:,1]

            #mov1 = 0.5
            #mov2 = 1-mov1
            #x0, x1 = int(mov1*np.amin(x) + mov2*x0), int(mov1*np.amax(x) + mov2*x1)
            #xy0 = int(x[np.argmin(y)]*mov1 + mov2*xy0)
            #xy1 = int(x[np.argmax(y)]*mov1 + mov2*xy1)
            #y0, y1 = int(np.amin(y)*mov1 + mov2*y0), int(np.amax(y)*mov1 + mov2*y1)
            #yx0 = int(y[np.argmin(x)]*mov1 + mov2*yx0)
            #yx1 = int(y[np.argmax(x)]*mov1 + mov2*yx1)
            if str(a) != 'None':
                cnt = a[0]
                eps = 0.05 * cv2.arcLength(cnt, True)
                polydp = cv2.approxPolyDP(cnt, eps, True)
            #print(str(polydp)+"\n\n")
                if len(polydp) >= 4:
                    polydp = list(map(lambda x: x[0], polydp))
                    polydp = list(map(tuple, polydp))
                    cv2.line(frame, ((polydp[0])), ((polydp[1])), (255, 0, 0), 10)
                    cv2.line(frame, ((polydp[2])), ((polydp[1])), (255, 0, 0), 10)
                    cv2.line(frame, ((polydp[2])), ((polydp[3])), (255, 0, 0), 10)
                    cv2.line(frame, ((polydp[0])), ((polydp[3])), (255, 0, 0), 10)
                    print(42/(((polydp[0][0]-polydp[1][0])**2+(polydp[0][1]-polydp[1][1])**2)**0.5)/6)




            #cv2.line(frame, (xy0,y0), (x0,yx0),(255, 0, 0), 10)
            #cv2.line(frame, (x1, yx1), (xy0, y0), (255, 0, 0), 10)
            #cv2.line(frame, (xy1, y1), (x0, yx0), (255, 0, 0), 10)
            #cv2.line(frame, (xy1, y1), (x1, yx1), (255, 0, 0), 10)
#
            #cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2, 1)
            if not ok:
                raise Exception('error occured in reading video')


            if True:

                # Display result
                cv2.imshow("Tracking", frame)

                # Exit if ESC pressed
                k = cv2.waitKey(1) & 0xff
                if k == 27:
                    break

    cv2.destroyAllWindows()

def corners(im:np.ndarray) -> np.ndarray:
    return cv2.filter2D(im, -1, np.array([[-1,1],[1,-1]]))

def edges(im:np.ndarray) -> np.ndarray:
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]))

def sharpen(im:np.ndarray) -> np.ndarray:
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))

def blur(im:np.ndarray) -> np.ndarray:
    return cv2.filter2D(im, -1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])/9)

def blue(im:np.ndarray) -> np.ndarray:
    return im[:,:,0]

def green(im:np.ndarray) -> np.ndarray:
    return im[:,:,1]

def red(im:np.ndarray) -> np.ndarray:
    return im[:,:,2]

def gray(im:np.ndarray) -> np.ndarray:
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

def hein(x):
    x = qsort(x)
    try:
        return (x[0]+x[1]+x[2])/3
    except:
        return x[0]

def bsort(lis):
    for i in range(len(lis)-1):
        if lis[i] > lis[i+1]:
            j = 0
            while i-j >=0 and lis[i-j] >= lis[i-j+1]:
                lis[i-j], lis[i-j+1] = lis[i-j+1], lis[i-j]
                j += 1
    return list(lis)


def qsort(lis):
    if len(lis) <= 1:
        return lis
    val = lis[0]
    lis = lis[1:]
    return qsort(list(filter(lambda a: a <= val, lis))) + [val] + qsort(list(filter(lambda a: a > val, lis)))


if __name__ == '__main__':
    main()