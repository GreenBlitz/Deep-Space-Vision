import cv2

video = cv2.VideoCapture(1)  # set this to the path to the video file

# Exit if video not opened.
if not video.isOpened():
    raise Exception('error occured in opening video')

# Read first frame

ok, frame = video.read()
