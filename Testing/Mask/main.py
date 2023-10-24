import cv2
import numpy as np

# read input image
bg = cv2.imread('bgp.jpg')

cap = cv2.VideoCapture(0)

# define range of blue color in HSV
lower_blue = np.array([100,60,40])
upper_blue = np.array([130,255,255])

while True:
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a mask. Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    maskinv = cv2.bitwise_not(mask)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(frame,frame, mask= maskinv)
    bgtmp = cv2.bitwise_and(bg,bg, mask= mask)
    result = cv2.addWeighted(bgtmp, 1, result, 1, 0)

    cv2.imshow('Masked Image',result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()