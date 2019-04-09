from utils.net import *
from utils import *


def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red, green, blue = params
    return cv2.inRange(frame, (int(red[0]), int(green[0]), int(blue[0])), (int(red[1]), int(green[1]), int(blue[1])))


def main():
    server = TCPStreamClient(ip='10.45.90.8', port=5801, fx=2, fy=2)
    while True:
        frame = server.get_frame()
        cv2.imshow('window', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('r'):
            bbox = cv2.selectROI('window', frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            ftag = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
            med = np.median(ftag, axis=(0, 1)).astype(int)
            stdv = np.array([10, 40, 40])
            params = np.vectorize(lambda x: min(255, max(0, x)))(np.array([med - stdv, med + stdv])).T
            break
        if k == ord('c'):
            break
    cv2.destroyAllWindows()
    print(list(map(list, params)))
    while True:
        frame = server.get_frame()
        cv2.imshow('threshold', threshold(frame, params.astype(int)))
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
