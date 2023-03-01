import cv2

cap = cv2.VideoCapture(0)

name = input("Enter Name: ")

while True:
    ret, frame = cap.read()

    cv2.imshow("Frame", frame)

    if cv2.waitKey(0) & 0xFF == ord('c'):
        cv2.imwrite("faces/" + name + ".jpg", frame)
        break

cap.release()