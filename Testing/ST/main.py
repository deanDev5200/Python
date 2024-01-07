import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=2, modelComplexity=1, minTrackCon=0.7, detectionCon=0.7)
video = cv2.VideoCapture(0)
rightMidMCP = (0, 0)
rightIndPIP = (0, 0)
leftMidMCP = (0, 0)
leftIndPIP = (0, 0)

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, True, False)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            if hand["type"] == "Right":
                rightMidMCP = (lmList[10][0], lmList[10][1])
                rightIndPIP = (lmList[6][0], lmList[6][1])
                print(rightMidMCP)
            else:
                leftMidMCP = (lmList[10][0], lmList[10][1])
                leftIndPIP = (lmList[6][0], lmList[6][1])
                #print(leftMidMCP)

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
          
video.release()
cv2.destroyAllWindows()