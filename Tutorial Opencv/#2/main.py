import cv2, os
__path__ = __file__[0:len(__file__)-len(os.path.basename(__file__))]


img = cv2.imread(__path__ + 'kangguru.jpg')
img = cv2.resize(img, (500, 500))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (51, 51), 0)

cv2.imshow('Image', img)
cv2.imshow('Gray', gray)
cv2.imshow('Blur', blur)

cv2.waitKey(0)
