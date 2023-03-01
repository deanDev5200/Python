import torch
import cv2
from PIL import Image

model = torch.hub.load('ultralytics/yolov5', 'custom', path='cascade/YOLOv5/Arduino.pt')
videodims = (640,480)
fourcc = cv2.VideoWriter_fourcc(*'avc1')    
video = cv2.VideoWriter("test.mp4",fourcc, 30,videodims)
#cap = cv2.VideoCapture('data/tes.mp4')
img = cv2.imread('data/Arduino.jpg')
while True:
    #_, img = cap.read()
    try:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img_rgb)
        im_pil2 = Image.fromarray(img_rgb)
        results = model(im_pil)
    
        video.write(cv2.cvtColor(results.imgs[0], cv2.COLOR_RGB2BGR))
    except:
        print("Ye be suud")
        video.release()
        break