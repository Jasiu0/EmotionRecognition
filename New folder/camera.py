__author__ = 'Jasiu'
import cv2

face_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_mcs_mouth.xml')
nose_cascade = cv2.CascadeClassifier('C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_mcs_nose.xml')

print face_cascade
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    #for (x, y, w, h) in faces:
    #   cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

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

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
