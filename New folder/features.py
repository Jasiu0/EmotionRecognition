#import numpy as np
import cv2
from PIL import Image
from random import randint
import sys

procent_s = 0.001
procent_n = 0.001
procent_e = 0.0005

face_cascade = cv2.CascadeClassifier('C:\Users\Jasiu\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\Users\Jasiu\Downloads\opencv\sources\data\haarcascades\haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('C:\Users\Jasiu\Downloads\opencv\mouth.xml')
nose_cascade = cv2.CascadeClassifier('C:\Users\Jasiu\Downloads\opencv\mnose.xml')

img = cv2.imread('11.jpg')
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

# ///////////////////////////////////////////////////////////// OBRAZ /////////////////////////////////////////////////
im = Image.open('11.jpg') #Can be many different formats.
pix = im.load()
[wymiar_x , wymiar_y] = im.size
wymiar_xy = wymiar_x * wymiar_y
print wymiar_xy

# ///////////////////////////////////////////////////////////// SMILE /////////////////////////////////////////////////
for (sx,sy,sw,sh) in smile:
    print sx,sy,sw,sh
zmiana =int( wymiar_xy  * procent_s)
print zmiana


zmiany = 0
while zmiany < zmiana:
    x_nowy = randint(sx,sx+sw)
    y_nowy = randint(sy,sy+sh)
    pix[x+x_nowy,y+y_nowy] = (randint(0,255),randint(0,255),randint(0,255))
    zmiany  = zmiany + 1

#im.save('po'+'1'+'.jpg', "JPEG")
#print zmiany

# ///////////////////////////////////////////////////////////// nose /////////////////////////////////////////////////
for (nx,ny,nw,nh) in nose:
    print nx,ny,nw,nh
zmiana =int( wymiar_xy  * procent_n)
print zmiana


zmiany = 0
while zmiany < zmiana:
    x_nowy = randint(nx,nx+nw)
    y_nowy = randint(ny,ny+nh)
    pix[x+x_nowy,y+y_nowy] = (randint(0,255),randint(0,255),randint(0,255))
    zmiany  = zmiany + 1

#im.save('po'+'1'+'.jpg', "JPEG")
#print zmiany

# ///////////////////////////////////////////////////////////// eyes /////////////////////////////////////////////////
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
     print ex,ey,ew,eh
     zmiana =int( wymiar_xy  * procent_e)
     print zmiana


     zmiany = 0
     while zmiany < zmiana:
        x_nowy = randint(ex,ex+ew)
        y_nowy = randint(ey,ey+eh)
        pix[x+x_nowy,y+y_nowy] = (randint(0,255),randint(0,255),randint(0,255))
        zmiany  = zmiany + 1

quality_val = 100
im.save('po_11_'+'all'+'.jpg', "JPEG", subsampling=0, quality = quality_val)
print zmiany