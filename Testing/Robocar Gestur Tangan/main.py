from cvzone.HandTrackingModule import HandDetector
import cv2
import httpx

class MainClass:
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.5, maxHands=2)
    i = 0

    def run(self):
        while True:
            success, img = MainClass.cap.read()
            hands, img = MainClass.detector.findHands(img)

            if hands:
                hand = hands[0]
                lmList = hand["lmList"]

                if lmList:
                    fingers = MainClass.detector.fingersUp(hand)
                    print(fingers)
                    if fingers == [0,1,1,0,0] and MainClass.i != 1:
                        httpx.get("http://192.168.4.1/set?a=1")
                        MainClass.i = 1
                        print('1')
                    elif fingers == [0,1,0,0,0] and MainClass.i != 2:
                        httpx.get("http://192.168.4.1/set?a=3")
                        MainClass.i = 2
                    elif fingers == [0,0,0,0,1] and MainClass.i != 3:
                        httpx.get("http://192.168.4.1/set?a=2")
                        MainClass.i = 3
                    elif fingers == [1,0,0,0,0] and MainClass.i != 4:
                        httpx.get("http://192.168.4.1/set?a=4")
                        MainClass.i = 4
                    elif (fingers == [1,1,1,1,1] or fingers == [0,0,0,0,0]) and MainClass.i != 0:
                        httpx.get("http://192.168.4.1/set?a=0")
                        MainClass.i = 0

            cv2.imshow("Frame", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        MainClass.cap.release()
        cv2.destroyAllWindows()

t = MainClass()
t.run()