from cvzone.HandTrackingModule import HandDetector
import cv2
import math
from selenium import webdriver 
import time

class MainClass:
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.5, maxHands=2)
    driver = webdriver.Edge()
    driver.set_window_size(1280, 720)
    currPix = 1

    driver.get("https://chrome.google.com/webstore/category/extensions")

    def run(self):
        while True:
            success, imgraw = self.cap.read()
            hands, img = self.detector.findHands(imgraw)

            if hands:
                hand = hands[0]
                lmList = hand["lmList"]
                if len(lmList) != 0:
                    x1, y1 = lmList[4][0], lmList[4][1]
                    x2, y2 = lmList[8][0], lmList[8][1]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                    length = math.hypot(x2 - x1, y2 - y1)

                    if length < 50:
                        self.driver.execute_script("window.scrollTo(0, {multi}*{i});".format(multi=35, i=self.currPix))  
                        self.currPix += 1

                        time.sleep(0.00001)
                        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                    
                    if length > 150:
                        if (self.currPix > 1):
                            self.driver.execute_script("window.scrollTo(0, {multi}*{i});".format(multi=35, i=self.currPix))  
                            self.currPix -= 1

                        time.sleep(0.00001)
                        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

            cv2.imshow("Frame", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

t = MainClass()
t.run()