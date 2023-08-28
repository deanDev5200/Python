import glob
import numpy as np
import pynput
import winsound
import cv2
from mss import mss
from time import sleep
from PIL import Image

count = 0
mouse = pynput.mouse.Controller()
def move_smooth(xm, ym, t):
    for i in range(t):
        if i < t/2:
            h = i
        else:
            h = t - i
        mouse.move(h*xm, h*ym)
        sleep(1/60)

mon = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
move_smooth(0, 1, 10)
with mss() as sct:
    while True:
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB', 
            (screenShot.width, screenShot.height), 
            screenShot.rgb, 
        )
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # lower range of diamond color in HSV
        lower_range = (82, 120, 120)

        # upper range of diamond color in HSV
        upper_range = (92, 255, 255)
        mask = cv2.inRange(hsv_img, lower_range, upper_range)
        color_image = cv2.bitwise_and(img, img, mask=mask)

        gray_version = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        if cv2.countNonZero(gray_version) == 0:
            print("Error")
        else:
            winsound.Beep(1000, 100)
            
            print("Image is fine")
        cv2.imwrite(f"Testing/MC/Bot/result/{count}.jpg", color_image)
        cv2.imshow('muhahahahahhah', color_image)
        count = count + 1
        if cv2.waitKey(33) & 0xFF in (
            ord('q'),
            27,
        ):
            break
        sleep(0.1)
img_array = []
for filename in glob.glob('D:/Python/Testing/MC/Bot/result/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()