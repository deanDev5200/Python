import cv2
from math import sqrt

posorigin = (250, 250)
testpos = (200, 200)
btnr = 60

def check(xpos, ypos, xorigin, yorigin):
    inside = False
    if ypos < yorigin+btnr:
        if xpos < xorigin:
            minX = xorigin-int(sqrt((btnr*btnr)-((ypos-yorigin)*(ypos-yorigin))))
            if xpos > minX:
                inside = True
        else:
            minX = xorigin+int(sqrt((btnr*btnr)-((ypos-yorigin)*(ypos-yorigin))))
            if xpos < minX:
                inside = True
    return inside

testimg = cv2.imread('tes.jpg')

testimg = cv2.circle(testimg, posorigin, btnr, (0,0,0), -1)
testimg = cv2.circle(testimg, testpos, 5, (0,0,255), -1)
print(check(testpos[0], testpos[1], posorigin[0], posorigin[1]))
cv2.imshow('gg', testimg)
cv2.waitKey(0)
