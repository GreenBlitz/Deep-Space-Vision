from utils.net import *
from utils import *
from models import *
import time
import pickle


def main():
    conn = TableConn(ip='10.45.90.2', table_name='vision')
    while True:
        frame = conn.get('frame')
        if frame != None:
            frame = pickle.loads(frame)
            frame = cv2.imdecode(frame, -1)
            # cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 2, (0, 255, 0), 2)
            cv2.imshow('stream', frame)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()
