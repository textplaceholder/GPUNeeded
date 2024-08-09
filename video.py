import cv2
import numpy as np
from yolodetect import YoloDetect

#contain polygon points
points = []

model = YoloDetect()

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1600)

def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


def draw_polygon (frame, points):
    for point in points:
        frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)

    frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
    return frame

detect = False

while True:
    retval,frame = video.read()
    frame = cv2.flip(frame, 1)

    frame = draw_polygon(frame, points)

    if detect:
        frame = model.detect(frame= frame, points= points)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('e'):
        points.append(points[0])
        detect = True

    #show feed
    cv2.imshow("Intrusion Warning. E to start. Q to quit", frame)

    cv2.setMouseCallback('Intrusion Warning. E to start. Q to quit', handle_left_click, points)

video.stop()
cv2.destroyAllWindows()