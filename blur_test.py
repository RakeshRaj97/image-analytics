import cv2
import face_recognition
import numpy as np

img = cv2.imread("download.png")
face_locations = face_recognition.face_locations(img)
list =[]
for i in face_locations:
  for j in i:
    list.append(i)

top_left = (list[0][3], list[0][0])
bottom_right = (list[0][1], list[0][2])
w, h, _ = img.shape
blurred_img = cv2.GaussianBlur(img, (21, 21), 0)

mask = np.zeros((w, h, _), dtype=np.uint8)
mask = cv2.rectangle(mask, top_left , bottom_right, ([255, 255, 255]), -1)

out = np.where(mask==np.array([255, 255, 255]), img, blurred_img)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow("image", out)

cv2.waitKey(0)
cv2.destroyAllWindows()
