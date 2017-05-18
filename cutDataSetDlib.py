import cv2
import glob
import dlib

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]  # Define emotions

detector = dlib.get_frontal_face_detector()
def detect_faces(emotion):
    files = glob.glob("C:\organizedDataSet\\" + emotion + "\\*")  # Get list of all images with emotion
    print files
    filenumber = 0
    for f in files:
        print f
        frame = cv2.imread(f)  # Open image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # Detect face using 4 different classifiers
        clahe_image = clahe.apply(gray)
        # c = cv2.resize(gray, (350,350))
        detections = detector(clahe_image, 1)

        for k,d in  enumerate(detections):
            print d.left(), d.top(), d.right(), d.bottom()
            xr = d.right()
            xl = d.left()
            yt = d.top()
            yb = d.bottom()
            gray = gray[yt:yb, xl:xr]
            print "face found in file: %s" % f

            try:
                out = cv2.resize(gray, (350, 350))  # Resize face so all images have same size
                cv2.imwrite("C:\cutDataSetDlib\\%s\\%s.jpg" % (emotion, filenumber), out)  # Write image
                print "zapisanie"
            except:
                print "nope"
                pass  # If error, pass file
        filenumber += 1  # Increment image number


for emotion in emotions:
    detect_faces(emotion)  # Call functiona