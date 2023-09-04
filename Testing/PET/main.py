from ultralytics import YOLO
import cv2
import socket

def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

print(get_ip())

model = YOLO("yolov8n.pt")
detections = []
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    detections = []
    results = model(source='images/bottles.jpg')

    for detection in results[0].boxes:
        class_index = detection.cls
        detections.append(int(class_index[0]))

    for p in detections:
        if p == 75:
            print("Yes")
        else:
            print("No")
    if detections == -1:
        break

cap.release()