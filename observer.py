
import sys
import cv2
import os




path_img = sys.argv[1]

img = cv2.imread(path_img)

print(path_img)
print(img.shape)


cv2.imshow(path_img, img)


cv2.waitKey(0)