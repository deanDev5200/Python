import cv2

img = cv2.imread('kangguru.jpg')
img = cv2.resize(img, (500, 500))
img = cv2.flip(img, 1)
img = cv2.GaussianBlur(img, (11, 11), 0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('image', img)
cv2.imshow('gray', gray)

cv2.imwrite('tes.jpg', gray)

tes = cv2.imread('tes.jpg')
cv2.imshow('tes.jpg', tes)

cv2.waitKey(0)
