import cv2
import numpy as np
from playsound import playsound


# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))



# cap=cv2.VideoCapture(0)
# while(True):
#     ret,frame=cap.read()
#     gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame',gray)
#     cv2.waitKey(0)
#     grayImage=gray
def warning(total_person):
    if total_person>3:
        playsound('warning.mp3')
        cv2.imshow("Image", img)

img = cv2.imread('groupphoto1.jpg')

img = cv2.resize(img, None, fx=0.2, fy=0.2)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
total_person=0
class_ids = []
confidences = []
boxes = []
personcounter=[]
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            # print(class_ids)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# print(indexes)
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        if label=='person':
            personcounter.append(1)
        color = colors[class_ids[i]]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        total_person = personcounter.count(1)

cv2.imshow("Image", img)
cv2.waitKey(0)
print(total_person)
if total_person>5:
    warning(total_person)
cv2.destroyAllWindows()

# cv2.imshow("Image", img)
