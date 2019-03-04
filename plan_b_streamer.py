from utils.net import *
from utils import *
from models import *
import time
import pickle


def main():
    conn = TableConn(ip='10.45.90.2', table_name='vision')
    camera = Camera(0, LIFECAM_3000)
    camera.resize(0.3, 0.3)
    max_fps = 20
    prev_time = 0
    while True:
        if (time.time() - prev_time) * max_fps < 1:
            continue
        ok, frame = camera.read()
        frame = cv2.imencode('.jpg', frame)
        frame = pickle.dumps(frame)
        conn.set('frame', frame)
        prev_time = time.time()


if __name__ == '__main__':
    main()
