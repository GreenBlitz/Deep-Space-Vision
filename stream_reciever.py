from utils.net import TCPStreamClient, cv2


def main():
    client = TCPStreamClient(ip='10.45.90.8', port=5801, fx=2, fy=2)
    while True:
        frame = client.get_frame()
        if frame is not None:
            cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 2, (0, 255, 0), 2)
            cv2.imshow('stream', frame)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()
