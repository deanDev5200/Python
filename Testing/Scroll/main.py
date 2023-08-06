from cvzone.HandTrackingModule import HandDetector
import cv2
import math
from pynput.mouse import Controller
import time

mouse = Controller()
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.3, maxHands=1)

while True:
    success, imgraw = cap.read()
    hands, img = detector.findHands(imgraw)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        if len(lmList) != 0:
            x1, y1 = lmList[4][0], lmList[4][1]
            x2, y2 = lmList[8][0], lmList[8][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    
            cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            length = math.hypot(x2 - x1, y2 - y1)

            if length < 50:
                mouse.scroll(0, 1)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
            elif length > 150:
                mouse.scroll(0, -1)
                cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            else:
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

    time.sleep(0.016)

    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()