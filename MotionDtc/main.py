import cv2
import serial
import time

face_cascade = cv2.CascadeClassifier('MotionDtc/haarcascade_frontalface_default.xml')
pix_off = 50

ser = serial.Serial("COM6", 9600)
cap = cv2.VideoCapture(0)
rettmp, imgtmp = cap.read()
wh = (imgtmp.shape[0], imgtmp.shape[1])
center = (wh[0]/2, wh[1]/2)
print(wh, center)
time.sleep(1.3)
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cmdtmp = ""
        if x+(w/2) < center[0]-10:
            cmdtmp += "+x"
        if x+(w/2) > center[0]+10:
            cmdtmp += "-x"
        if y+(h/2) < center[1]-10:
            cmdtmp += ":-y"
        if y+(h/2) > center[1]+10:
            cmdtmp += ":+y"
        if cmdtmp != "":
            print(cmdtmp);
            ser.write(cmdtmp.encode())
        time.sleep(1)
        


    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()