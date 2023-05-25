import cv2
import serial
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
pix_off = 50
serOpen = False
try:
    ser = serial.Serial("COM6", 9600)
    print('connect')
    serOpen = True
except:
    pass
cap = cv2.VideoCapture(0)
rettmp, imgtmp = cap.read()
wh = (imgtmp.shape[1], imgtmp.shape[0])
center = (int(wh[0]/2), int(wh[1]/2))
print(wh, center)
time.sleep(1.3)
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(img,(center[0], center[1]-20),(center[0],center[1]+20),(0,255,0),2)
    cv2.rectangle(img,(center[0]-20, center[1]),(center[0]+20,center[1]),(0,255,0),2)
    cv2.rectangle(img,(center[0]-7, center[1]-7),(center[0]+7,center[1]+7),(255,0,255))
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)
    for (x,y,w,h) in faces:
        faceloc = (int(x+(w/2)), int(y+(h/2)))
        cv2.circle(img,faceloc,3,(0,0,255),4)
        cmdtmp = ""
        if faceloc[0] < center[0]-7:
            cmdtmp += "+"
        elif faceloc[0] > center[0]+7:
            cmdtmp += "-"
        
        if faceloc[1] < center[1]-7:
            cmdtmp += "-"
        elif faceloc[1] > center[1]+7:
            cmdtmp += "+"
        if len(cmdtmp) > 0:
            cmdtmp += "\n"
            print(cmdtmp)
            if serOpen:
                ser.write(cmdtmp.encode()) # type: ignore
        time.sleep(0.03)
        


    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()