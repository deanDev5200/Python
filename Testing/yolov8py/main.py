from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
model.predict(
   source=0,
   conf=0.25,
   show=True
)

cv2.waitKey(0)
