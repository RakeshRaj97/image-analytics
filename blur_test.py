import cv2
import face_recognition
import numpy as np
from shapely.geometry import Polygon

img = cv2.imread("test4.jpeg")
a, b, c = img.shape

face_locations = face_recognition.face_locations(img)
list =[]
for i in face_locations:
  for j in i:
    list.append(i)


def calculate_iou(box_1, box_2):
    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)
    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou

box_1 = [[list[0][3], list[0][0]], [list[0][1], list[0][0]], [list[0][1], list[0][2]], [list[0][3], list[0][2]]]
box_2 = [[0, 0], [a, 0], [a, b], [0, b]]

iou = calculate_iou(box_1, box_2)
iou = round(iou*100)
print(iou)
top_left = (list[0][3], list[0][0])
bottom_right = (list[0][1], list[0][2])
w, h, _ = img.shape
blurred_img = cv2.GaussianBlur(img, (21, 21), 0)

mask = np.zeros((w, h, _), dtype=np.uint8)
mask = cv2.rectangle(mask, top_left , bottom_right, ([255, 255, 255]), -1)

out = np.where(mask==np.array([255, 255, 255]), img, blurred_img)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(out, str(iou)+'%', (50,50), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow("image", out)

cv2.waitKey(0)
cv2.destroyAllWindows()

