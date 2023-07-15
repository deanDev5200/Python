from ultralytics import YOLO
from PIL import Image
import cv2

cap = cv2.VideoCapture(0)
model = YOLO('yolov8n.pt')

while True:
   ret, img = cap.read()
   color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   pilimg = Image.fromarray(color_coverted)
   model.predict(
      source=pilimg,
      conf=0.5,
      show = True
   )
