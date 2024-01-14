import time
startTime = time.time()
import torch, cv2
print('torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))
from ultralytics import YOLO
model = YOLO('best.pt')
import keyboard

model_path = 'D:\Python\Testing\ST\gesture_recognizer.task' 
video = cv2.VideoCapture(0)
scene = False

while True:
    num = 0
    _, img = video.read()

    results = model.predict(img, classes=1, stream=True)
    for r in results:
        num = len(r.boxes.cls.tolist())
        view = cv2.putText(r.orig_img, str(r.boxes.xywh.tolist()), (160, 360), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 6)
        view = cv2.putText(view, str(r.boxes.xywh.tolist()), (160, 360), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        if len(r.boxes.xyxy.tolist())>0:
            view = cv2.rectangle(view, (int(r.boxes.xyxy.tolist()[0][0]), int(r.boxes.xyxy.tolist()[0][1])), (int(r.boxes.xyxy.tolist()[0][2]), int(r.boxes.xyxy.tolist()[0][3])), (255, 0, 0), 5)

    cv2.imshow("epep", view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if num > 0:
        if not scene:
            keyboard.press("Ctrl+Home")
            time.sleep(0.5)
            keyboard.release("Ctrl+Home")
            scene = True
        else:
            keyboard.press("Ctrl+]")
            time.sleep(0.5)
            keyboard.release("Ctrl+]")
            scene = False


video.release()
