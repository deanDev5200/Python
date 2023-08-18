import cv2
from cvzone.HandTrackingModule import HandDetector
import requests

detector = HandDetector(maxHands=1, detectionCon=0.5)
video = cv2.VideoCapture(0)
i = 0
while True:
    _, img = video.read()
    hands, img = detector.findHands(img)
    try:
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            if lmList:
                fingers = detector.fingersUp(hand)
                if fingers == [0, 1, 1, 0, 0] and i != 1:
                    requests.get('http://192.168.4.1/set?a=1', timeout=0.5)
                    i = 1
                elif fingers == [0, 0, 0, 0, 1] and i != 2:
                    requests.get('http://192.168.4.1/set?a=2', timeout=0.5)
                    i = 2
                elif fingers == [0, 1, 0, 0, 0] and i != 3:
                    requests.get('http://192.168.4.1/set?a=3', timeout=0.5)
                    i = 3
                elif fingers == [1, 0, 0, 0, 0] and i != 4:
                    requests.get('http://192.168.4.1/set?a=4', timeout=0.5)
                    i = 4
                elif fingers != [1, 0, 0, 0, 0] and fingers != [0, 1, 1, 0, 0] and fingers != [0, 1, 0, 0, 0] and fingers != [0, 0, 0, 0, 1] and i != 0:
                    requests.get('http://192.168.4.1/set?a=0', timeout=0.5)
                    i = 0
        elif i != 0:
            requests.get('http://192.168.4.1/set?a=0', timeout=0.1)
            i = 0
    except:
        pass
    cv2.imshow("Video", img)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
          
video.release()
cv2.destroyAllWindows()