import torch, cv2, time
print('torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))
from ultralytics import YOLO
model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

while True:
    num = 0
    _, frame = cap.read()
    results = model.predict(frame, classes=1, stream=True)
    time.sleep(0.1)
    for r in results:
        num = len(r.boxes.cls)
    if len(r.boxes.cls) > 0:
        break


cap.release()
