from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2
from telegram_utils import send_telegram
from datetime import datetime,timezone
import threading


from ultralytics import YOLO

def isInside(points, centroid):
    polygon = Polygon(points)
    centroid = Point(centroid)
    print(polygon.contains(centroid))
    return polygon.contains(centroid)


class YoloDetect():
    def __init__(self, detect_class="person", frame_width=1280, frame_height=720):
        self.detect_class = detect_class
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.conf_threshold = 0.5
        self.nms_threshold = 0.4
        self.model = YOLO('trained_model.pt')
        self.last_alert = None
        self.alert_telegram_each = 15  # 15s 1 message
        

    def draw_prediction(self, img, class_name, x, y, x_plus_w, y_plus_h, points):
        color = (0, 255, 0)
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(img, class_name, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        #calc centroid
        centroid = ((x + x_plus_w) // 2, (y + y_plus_h) // 2)
        cv2.circle(img, centroid, 5, color, -1)

        if isInside(points, centroid):
            img = self.alert(img)

        return isInside(points, centroid)
#thong bao
    def alert(self, img):
        cv2.putText(img, "ALARM!!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #send telegram over 15 second
        if (self.last_alert is None) or (
                (datetime.now(timezone.utc) - self.last_alert).total_seconds() > self.alert_telegram_each):
            self.last_alert = datetime.now(timezone.utc)
            cv2.imwrite("alert.png",img)

            thread = threading.Thread(target=send_telegram)
            thread.start()


        return img
#
    def detect(self, frame, points):
        #frame to tensor
        results = self.model(frame)

        #extract detection
        for result in results:
            for detection in result.boxes:
                x1, y1, x2, y2 = detection.xyxy[0]
                conf = detection.conf[0]
                class_id = int(detection.cls[0])
                if conf >= self.conf_threshold and self.model.names[int(class_id)] == self.detect_class:
                    self.draw_prediction(frame, self.model.names[int(class_id)], int(x1), int(y1), int(x2), int(y2), points)

        return frame

    