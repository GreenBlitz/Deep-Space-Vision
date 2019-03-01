from models import *
from utils import *


def threshold(frame, params):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
    red, green, blue = params
    return cv2.inRange(frame, (int(red[0]), int(green[0]), int(blue[0])), (int(red[1]), int(green[1]), int(blue[1])))


def main():
    src = []
    boxes = []
    video = Camera(0, CameraData(0, 0))
    video.toggle_auto_exposure(0.25)
    video.set_exposure(-5)
    # video.resize(0.4, 0.4)

    while True:
        ok, frame = video.read()
        cv2.imshow('window', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('r'):
            bbox = cv2.selectROI('window', frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
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
        ok, frame = video.read()
        if not ok:
            print('not ok')
            continue
        cv2.imshow('threshold', threshold(frame, params.astype(int)))
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
