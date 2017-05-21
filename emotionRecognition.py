import cv2, glob, random, math, numpy as np, dlib, itertools
from sklearn.svm import SVC

emotions = ["anger", "contempt", "disgust", "fear", "happy", "neutral", "sadness", "surprise"]  # Emotion list
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:\Users\Jasiu\Downloads\shape_predictor_68_face_landmarks.dat")  # Or set this to whatever you named the downloaded file
clf = SVC(kernel='linear', probability=True,tol=1e-3)  # , verbose = True) #Set the classifier as a support vector machines with polynomial kernel


def get_files(emotion):  # Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("C:\cutDataSetDlib\\%s\\*" % emotion)
    random.shuffle(files)
    training = files[:int(len(files) * 0.8)]  # get first 80% of file list
    prediction = files[-int(len(files) * 0.2):]  # get last 20% of file list
    return training, prediction


def get_landmarks(image):
    detections = detector(image, 1)
    for k, d in enumerate(detections):  # For all detected face instances individually
        shape = predictor(image, d)  # Draw Facial Landmarks with the predictor class
        xlist = []
        ylist = []
        for i in range(1, 68):  # Store X and Y coordinates in two lists
            xlist.append(float(shape.part(i).x))
            ylist.append(float(shape.part(i).y))

        xmean = np.mean(xlist)  # Get the mean of both axes to determine centre of gravity
        ymean = np.mean(ylist)
        xcentral = [(x - xmean) for x in xlist]  # get distance between each point and the central point in both axes
        ycentral = [(y - ymean) for y in ylist]

        if xlist[26] == xlist[
            29]:  # If x-coordinates of the set are the same, the angle is 0, catch to prevent 'divide by 0' error in function
            anglenose = 0
        else:
            anglenose = int(math.atan((ylist[26] - ylist[29]) / (xlist[26] - xlist[29])) * 180 / math.pi)

        if anglenose < 0:
            anglenose += 90
        else:
            anglenose -= 90

        landmarks_vectorised = []
		print 'xcent:' +str(xcentral[1])
        for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
			print 'x:' +str(xcentral[1])
            landmarks_vectorised.append(x)
            landmarks_vectorised.append(y)
            meannp = np.asarray((ymean, xmean))
            coornp = np.asarray((z, w))
            dist = np.linalg.norm(coornp - meannp)
            anglerelative = (math.atan((z - ymean) / (w - xmean)) * 180 / math.pi) - anglenose
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append(anglerelative)

    if len(detections) < 1:
        landmarks_vectorised = "error"
    return landmarks_vectorised


def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training, prediction = get_files(emotion)
        # Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item)  # open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
            clahe_image = clahe.apply(gray)
            landmarks_vectorised = get_landmarks(clahe_image)
            if landmarks_vectorised == "error":
                pass
            else:
                training_data.append(landmarks_vectorised)  # append image array to training data list
                training_labels.append(emotions.index(emotion))

       # for item in prediction:
        #    image = cv2.imread(item)
         #   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          #  clahe_image = clahe.apply(gray)
           # landmarks_vectorised = get_landmarks(clahe_image)
            #if landmarks_vectorised == "error":
             #   pass
            #else:
             #   prediction_data.append(landmarks_vectorised)
              #  prediction_labels.append(emotions.index(emotion))

    return training_data, training_labels#, prediction_data, prediction_labels


accur_lin = []
#for i in range(0, 10):
print("Making sets %s" % 0)  # Make sets by random sampling 80/20%
training_data, training_labels = make_sets()

npar_train = np.array(training_data)  # Turn the training set into a numpy array for the classifier
npar_trainlabs = np.array(training_labels)
print("training SVM linear %s" % 0)  # train SVM
clf.fit(npar_train, training_labels)
print npar_train
print training_labels

print("getting accuracies %s" % 0)  # Use score() function to get accuracy
    #npar_pred = np.array(prediction_data)
    #pred_lin = clf.score(npar_pred, prediction_labels)
    ##print "linear: ", pred_lin
    #accur_lin.append(pred_lin)  # Store accuracy in a list

#print("Mean value lin svm: %.3f" % np.mean(accur_lin))  # Get mean accuracy of the 10 runs
video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    #frame = cv2.imread('C:\Users\Jasiu\Downloads\untitled2\untitled2\\3.jpg')
    #frame = cv2.imread('C:\Users\Jasiu\Pictures\Camera Roll\\3.jpg')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray)
    detections = detector(clahe_image, 1)  # Detect the faces in the image

    for k, d in enumerate(detections):  # For each detected face
     #   xr = d.right()
      #  xl = d.left()
       # yt = d.top()
        #yb = d.bottom()
        #gray = gray[yt:yb, xl:xr]
        #clahe_image = clahe.apply(gray)
        #detections = detector(clahe_image, 1)
        #print str(k) + " " + str(d)
        #for a, b in enumerate(detections):
            shape = predictor(clahe_image, d)  # Get coordinates
            for i in range(1, 68):  # There are 68 landmark points on each face
                cv2.circle(gray, (shape.part(i).x, shape.part(i).y), 1, (0, 0, 255), thickness=2)  # For each point, draw a red circle with thickness2 on the original frame

    cv2.imshow("image", gray)  # Display the frame
    landmarks_vectorised = get_landmarks(clahe_image)

    if landmarks_vectorised == "error":
        pass
    else:
        pred_data = []
        pred_data.append(landmarks_vectorised)
        #print pred_data
        im = np.array(pred_data)
        pred = clf.predict_proba(im)
        #pred = clf.predict(im,0)

        print pred

    if cv2.waitKey(60) & 0xFF == ord('q'):  # Exit program when the user presses 'q'
        break