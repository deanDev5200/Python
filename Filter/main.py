from typing import Any
import keyboard
import cv2

face_cascade = cv2.CascadeClassifier('Filter/cascade.xml')

specs_ori = cv2.imread('Filter/data/glasses.png', -1)
specs_ori2 = cv2.imread('Filter/data/ironman.png', -1)
specs_ori3 = cv2.imread('Filter/data/spiderma.png', -1)
specs_ori4 = cv2.imread('Filter/data/1.png', -1)
videodims = (640,480)
fourcc = cv2.VideoWriter_fourcc(*'avc1')    
video = cv2.VideoWriter("test.mp4",fourcc, 30,videodims)
# Camera Init
cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FPS, 30)
mode = 0
maxMode = 3
def keypress(a: Any):
    global mode
    if a.name == '2':
        mode = 1
    elif a.name == '1':
        mode = 0
    elif a.name == '3':
        mode = 2
    elif a.name == '4':
        mode = 3

def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape
    rows, cols, _ = src.shape
    y, x = pos[0], pos[1]

    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src
keyboard.on_press(keypress)
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.2, 5, 0, (120, 120), (350, 350))
    
    for (x, y, w, h) in faces:
        if h > 0 and w > 0:
            if mode == 0:
                glass_symin = int(y + 2 * h / 50)
                glass_symax = int(y + 3.5 * h / 5)
                sh_glass = glass_symax - glass_symin
            

                face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]

                specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
            elif mode == 1:
                glass_symin = int(y + 0.4 * h / 50)
                glass_symax = int(y + 7 * h / 5)
                sh_glass = glass_symax - glass_symin
            

                face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]
                specs = cv2.resize(specs_ori2, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
            elif mode == 2:
                glass_symin = int(y + 0.4 * h / 50)
                glass_symax = int(y + 7 * h / 5)
                sh_glass = glass_symax - glass_symin
            
                 
                face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]
                specs = cv2.resize(specs_ori3, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
            elif mode == 3:
                glass_symin = int(y + 0.4 * h / 50)
                glass_symax = int(y + 7 * h / 5)
                sh_glass = glass_symax - glass_symin
            

                face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]
                specs = cv2.resize(specs_ori4, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
            transparentOverlay(face_glass_roi_color, specs)

    cv2.imshow('Window', img)
    video.write(img)

    k = cv2.waitKey(30) & 0xff
    if k == ord('q'):
        video.release()
        break

cap.release()
cv2.destroyAllWindows()