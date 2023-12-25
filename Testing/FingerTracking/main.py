import cv2
import random
from cvzone.HandTrackingModule import HandDetector
from time import sleep

detector = HandDetector(maxHands=1, detectionCon=0.82)
video = cv2.VideoCapture(0)
boxpos = (random.randint(200, 900), random.randint(200, 650))
boxsize = 30
boxcolor = (255, 0, 0)
boxpinch = False
tmpboxpos = boxpos
lastfpos = (0, 0)
posaddamount = (0, 0)
drag = False
score = 0

targetpos1 = (10, 10)
targetpos2 = (110, 110)
targetcolor = (0, 0, 255)

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    p1 = tuple(map(lambda i, j: i - j, tmpboxpos, (boxsize,boxsize)))
    p2 = tuple(map(lambda i, j: i + j, tmpboxpos, (boxsize,boxsize)))

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        xy1 = (lmList[4][0], lmList[4][1])
        xy2 = (lmList[8][0], lmList[8][1])
        center = (int((xy2[0]-xy1[0])/2+xy1[0]), int((xy2[1]-xy1[1])/2+xy1[1]))
        distance, imag, info = detector.findDistance(xy1, xy2, img)
        lastboxpinch = boxpinch
        
        if center[0] < p2[0] and center[0] > p1[0] and center[1] < p2[1] and center[1] > p1[1]:
            if distance < 70 and not drag:
                drag = True
            cv2.circle(img, center, 10, boxcolor, 3)

        
        if distance < 70 and drag:
            boxpinch = True
        else:
            drag = False
            boxpinch = False

        if not lastboxpinch and boxpinch:
            lastfpos = center
        elif not boxpinch and lastboxpinch:
            boxpos = tmpboxpos

        if boxpinch:
            posaddamount = tuple(map(lambda i, j: i - j, center, lastfpos))
            tmpboxpos = tuple(map(lambda i, j: i + j, boxpos, posaddamount))
            boxcolor = (0, 0, 255)
        else:
            boxcolor = (255, 0, 0)

    if boxpos[0] < targetpos2[0] and boxpos[0] > targetpos1[0] and boxpos[1] < targetpos2[1] and boxpos[1] > targetpos1[1]:
        targetcolor = (0, 255, 0)
    else:
        targetcolor = (0, 0, 255)

    cv2.rectangle(img, targetpos1, targetpos2, targetcolor, 5)
    cv2.rectangle(img, p1, p2, boxcolor, -1)
    cv2.putText(img, "Score: " + str(score), (10, 710), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if targetcolor == (0, 255, 0):
        score = score + 1
        boxpos = (random.randint(200, 900), random.randint(200, 650))
        tmpboxpos = boxpos
          
video.release()
cv2.destroyAllWindows()