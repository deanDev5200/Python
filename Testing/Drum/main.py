from cvzone.HandTrackingModule import HandDetector
from cvzone.Utils import overlayPNG
from math import sqrt
import cv2
import pygame

pygame.mixer.init()
snareSound = pygame.mixer.Sound('audio/wav/snare.wav')
tom1Sound = pygame.mixer.Sound('audio/wav/tom1.wav')
tom2Sound = pygame.mixer.Sound('audio/wav/tom2.wav')
tom3Sound = pygame.mixer.Sound('audio/wav/tom3.wav')
cap = cv2.VideoCapture(0)
drumImg = cv2.imread('Images/drum/drum.png', -1)
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=0, detectionCon=0.8, minTrackCon=0.4)

snareRadius = 90
snarePos = (480, 497)
tomRadius = 60
tom1Pos = (348, 391)
tom2Pos = (480, 318)
tom3Pos = (612, 391)
tapR = False
tapL = False

def check(xpos, ypos, xorigin, yorigin, buttonRadius):
    inside = False
    if xpos == xorigin and ypos == yorigin:
        return True
    else:
        if ypos < yorigin+buttonRadius and ypos > yorigin-buttonRadius:
            if xpos < xorigin:
                minX = xorigin-int(sqrt((buttonRadius*buttonRadius)-((ypos-yorigin)*(ypos-yorigin))))
                if xpos > minX:
                    inside = True
            else:
                minX = xorigin+int(sqrt((buttonRadius*buttonRadius)-((ypos-yorigin)*(ypos-yorigin))))
                if xpos < minX:
                    inside = True
        return inside
    
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=False)

    img = overlayPNG(img, drumImg)
    #img = cv2.circle(img, tom1Pos, tomRadius, (0, 0, 255), -1)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            #p1 = (lmList[17][0], lmList[17][1])
            #p2 = (lmList[5][0], lmList[5][1])
            pos = (lmList[8][0], lmList[8][1])
            dist = lmList[8][2]
            if dist > -60:
                img = cv2.putText(img, str(dist), pos, cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 5)
            else:
                img = cv2.putText(img, str(dist), pos, cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 5)

            img = cv2.putText(img, str(dist), pos, cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1)

            checkSnare = check(pos[0], pos[1], snarePos[0], snarePos[1], snareRadius)
            checkTom1 = check(pos[0], pos[1], tom1Pos[0], tom1Pos[1], tomRadius)
            checkTom2 = check(pos[0], pos[1], tom2Pos[0], tom2Pos[1], tomRadius)
            checkTom3 = check(pos[0], pos[1], tom3Pos[0], tom3Pos[1], tomRadius)

            if hand["type"] == "Right":
                if dist < -60 and not tapR:
                    tapR = True
                    if checkSnare:
                        snareSound.play()
                    elif checkTom1:
                        tom1Sound.play()
                    elif checkTom2:
                        tom2Sound.play()
                    elif checkTom3:
                        tom3Sound.play()
                    else:
                        tapR = False
                elif dist > -55 and tapR:
                    tapR = False
            else:
                if dist < -60 and not tapL:
                    tapL = True
                    if checkSnare:
                        snareSound.play()
                    elif checkTom1:
                        tom1Sound.play()
                    elif checkTom2:
                        tom2Sound.play()
                    elif checkTom3:
                        tom3Sound.play()
                    else:
                        tapL = False
                elif dist > -55 and tapL:
                    tapL = False

 
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break