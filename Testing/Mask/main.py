import cv2
import numpy as np
import cvzone

# read input image
img = cv2.imread('d.jpg')
bg = cv2.imread('bgp.jpg')

# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_yellow = np.array([100,60,40])
upper_yellow = np.array([130,255,255])

# Create a mask. Threshold the HSV image to get only yellow colors
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
maskinv = cv2.bitwise_not(mask) 

# Bitwise-AND mask and original image
result = cv2.bitwise_and(img,img, mask= maskinv)
bgtmp = cv2.bitwise_and(bg,bg, mask= mask)
result = cv2.addWeighted(bgtmp, 1, result, 1, 0)

# display the mask and masked image
cv2.imshow('Mask',mask)
cv2.waitKey(0)
cv2.imshow('Masked Image',result)
cv2.waitKey(0)
cv2.destroyAllWindows()