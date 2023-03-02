import cv2

img = cv2.imread('testimg.png')
img2 = cv2.resize(img, (500, 500))
while True:
    cv2.imshow('Gambar', img)
    cv2.imshow('Gambar 2', img2)

    if cv2.waitKey(1) == 27:
        break