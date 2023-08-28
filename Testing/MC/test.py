
import glob

import cv2


img_array = []
for filename in glob.glob('D:/Python/Testing/MC/Bot/result/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()