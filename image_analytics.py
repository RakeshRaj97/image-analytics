# import libraries
import cv2
import face_recognition
import numpy as np
from shapely.geometry import Polygon
import mouth_open
from fer import FER
import requests
from extract_url import image_url
from cognitive_api import cognitive_api

# extract image url from the linkedin profile url
profile_url = "https://www.linkedin.com/in/scottmorrisonmp/"
image_url = image_url(profile_url)

# download the image from image_url
img_data = requests.get(image_url).content
with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)

# load image
img = cv2.imread("image_name.jpg")
a, b, c = img.shape

# detect face locations and append the values to a list
face_locations = face_recognition.face_locations(img)
list = []
for i in face_locations:
    for j in i:
        list.append(i)

# Find all facial features in all the faces of an image
face_landmarks_list = face_recognition.face_landmarks(img)
top_lip = face_landmarks_list[0]['top_lip']
bottom_lip = face_landmarks_list[0]['bottom_lip']

# identify teeth visibility
teeth = mouth_open.check_mouth_open(top_lip, bottom_lip)


# method to calculate iou
def calculate_iou(box_1, box_2):
    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)
    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou


box_1 = [[list[0][3], list[0][0]], [list[0][1], list[0][0]], [list[0][1], list[0][2]], [list[0][3], list[0][2]]]
box_2 = [[0, 0], [a, 0], [a, b], [0, b]]


# method to find face quality
def face_quality(iou):
    if iou >= 50:
        return 'good'
    else:
        return 'too small'


# emotions
detector = FER()
emotion, score = detector.top_emotion(img)

# microsoft cognitive api to perform visual feature recognition
vis_feature = cognitive_api(image_url)

# get iou and face quality
iou = calculate_iou(box_1, box_2)
iou = round(iou * 100)
face_quality_ = face_quality(iou)

# blur background except face
top_left = (list[0][3], list[0][0])
bottom_right = (list[0][1], list[0][2])
w, h, _ = img.shape
blurred_img = cv2.GaussianBlur(img, (21, 21), 0)

mask = np.zeros((w, h, _), dtype=np.uint8)
mask = cv2.rectangle(mask, top_left, bottom_right, ([255, 255, 255]), -1)

out = np.where(mask == np.array([255, 255, 255]), img, blurred_img)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(out, "Face quality: " + str(face_quality_), (5, 50), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
cv2.putText(out, "Is teeth visible: " + str(teeth), (5, 70), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
cv2.putText(out, emotion + ":" + str(round(score * 100)) + "%", (5, 110), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
cv2.putText(out, vis_feature, (5, 130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow("image", out)

cv2.waitKey(0)
cv2.destroyAllWindows()
