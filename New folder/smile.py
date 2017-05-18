import cv2
#from PIL import Image
from random import randint
import sys

procent_s = 0.001
procent_n = 0.0001
procent_e = 0.0001

face_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascades\haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_mcs_mouth.xml')
nose_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_mcs_nose.xml')

img = cv2.imread('2.jpg')
#img = cv2.imread('11.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

    eyes = eye_cascade.detectMultiScale(roi_gray)
    smile = smile_cascade.detectMultiScale(roi_gray,
            scaleFactor= 1.7,
            minNeighbors=22,
            minSize=(25, 25))
    nose = nose_cascade.detectMultiScale(roi_gray,
            scaleFactor= 1.7,
            minNeighbors=22,
            minSize=(25, 25))
    for (ex,ey,ew,eh) in eyes:
         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    for (sx,sy,sw,sh) in smile:
         cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)
    for (nx,ny,nw,nh) in nose:
         cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(100,105,100),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()