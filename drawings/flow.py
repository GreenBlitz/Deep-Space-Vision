import cv2


def draw_flow(frame, contour, color=(255, 0, 0)):
    for i, c in enumerate(contour):
        cv2.arrowedLine(frame, tuple(c[0]), tuple(contour[(i + 1) % len(contour)][0]), color, 5)
