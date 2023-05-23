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
        faceloc = (x+(w/2), y+(h/2))
        cmdtmp = ""
        if faceloc[0] < center[0]-3:
            cmdtmp += "+"
        elif faceloc[0] > center[0]+3:
            cmdtmp += "-"
        
        if faceloc[1] < center[1]-3:
            cmdtmp += "-"
        elif faceloc[1] > center[1]+3:
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