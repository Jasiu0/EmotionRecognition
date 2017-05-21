import glob
import cv2
import dlib
import numpy
import math
from sklearn.svm import SVC

class EmotionRecognition():

	def runContinuous(self):
		print "cont"
		
	def runFixed(self, imageSource, predictor, pathToDataSet,classifier, emotions, \
	showImage, showFeaturePoints, outputStream, outputStreamDirectory):
		self.imageSource = imageSource
		self.predictor = predictor
		# inicjacja predykatora
		self.shapePredictor = dlib.shape_predictor(self.predictor)
		self.pathToDataSet = pathToDataSet
		self.classifier= classifier
		self.emotions = emotions
		self.showImage = showImage
		self.showFeaturePoints = showFeaturePoints
		self.outputStream = outputStream
		self.outputStreamDirectory = outputStreamDirectory
		# inicjacja detectora dlib
		self.detector = dlib.get_frontal_face_detector()
		clf = SVC(kernel='linear', probability=True,tol=1e-3) 
		
		print '\nStarting Training'
		trainingData, trainingLabels = self.makeTeachingSet()
		npar_train = numpy.array(trainingData)  # Turn the training set into a numpy array for the classifier
		npar_trainlabs = numpy.array(trainingLabels)
		print("training SVM linear %s" % 0)  # train SVM
		clf.fit(npar_train, trainingLabels)
		print 'Training Finished'
		video_capture = cv2.VideoCapture(0)
		while True:		
			age = raw_input("Your age? ")
			#image = cv2.imread(age)
			ret, image = video_capture.read()
							# Konwersja na skale szarosci
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
					# Zwiekszenie kontrastu
			clahePhoto = clahe.apply(gray)
					# Otrzymaj punkty charakterystyczne
			normalizedFeaturePoints = self.getFeaturePoints(clahePhoto)
			if normalizedFeaturePoints == "No face detected":
				pass
			else:
				pred_data = []
				pred_data.append(normalizedFeaturePoints)
				#print pred_data
				im = numpy.array(pred_data)
				pred = clf.predict_proba(im)
				#pred = clf.predict(im,0)

			print pred
	
	def runResearch(self):
		print 'Reasearch'
		
	def makeTeachingSet(self):
		trainingData = []
		trainingLabels = []
		for emotion in self.emotions:
			dataSetFiles = glob.glob(self.pathToDataSet + '\\' + emotion +'\\*')
			# Dla kazdego obrazu w zbiorze uczacym
			for file in dataSetFiles:
				# Otworz obraz
				image = cv2.imread(file)
				# Konwersja na skale szarosci
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
				# Zwiekszenie kontrastu
				clahePhoto = clahe.apply(gray)
				# Otrzymaj punkty charakterystyczne
				normalizedFeaturePoints = self.getFeaturePoints(clahePhoto)
				#print 'norm' + str(normalizedFeaturePoints)
				if normalizedFeaturePoints == "No face detected":
					pass
				else:
					# Dodawanie listy znormalizowanych punktow kontrolnych do zbioru
					trainingData.append(normalizedFeaturePoints)
					trainingLabels.append(self.emotions.index(emotion))
			print 'Training ' + emotion + ' emotion finished'

		return trainingData, trainingLabels#, prediction_data, prediction_labels


	def getFeaturePoints(self, photo):
		detections = self.detector(photo, 1)
		
		# Dla kazdej wykrytej twarzy
		for index,coordinates in  enumerate(detections):
			# Wykryj punkty kontrolne za pomoca predykatora
			shape = self.shapePredictor(photo, coordinates)
			# Listy z punktami na osi X i Y
			xList = []
			yList = []
			# Dla kazdego z 68 punktow charakterystycznych
			for featurePoint in range(1, 68):
				# Dodaj do list: xList i yList
				xList.append(float(shape.part(featurePoint).x))
				yList.append(float(shape.part(featurePoint).y))
				
			# Oblicz srodek ciezkosci obrazu dla obu osi
			xMean = numpy.mean(xList)
			yMean = numpy.mean(yList)
			# Oblicz odleglosc pomiedzy punktem a srodkiem ciezkosci dla kazdego z punktow w obu osiach
			xMeanDistance = [(x - xMean) for x in xList]
			yMeanDistance = [(y - yMean) for y in yList]
			# Jezeli punkty w osi x nosa sa w jednej osi kat wynosi 0, w innym przypadku liczymy kat
			print xList[26]
			print xList[29]
			print yList[26]
			print yList[29]
			if xList[26] == xList[29]:
				print '0'
				noseAngle = 0
			else:
				print ' '
				# int?
				noseAngle =  math.degrees(math.atan((yList[26] - yList[29]) / (xList[26] - xList[29])))

			if noseAngle < 0:
				noseAngle += 90
			else:
				noseAngle -= 90

			normalizedFeaturePoints = []
			for w, z in zip(xList, yList):
				normalizedFeaturePoints.append(x)
				normalizedFeaturePoints.append(y)
				meannp = numpy.asarray((yMean, xMean))
				#print 'mean: ' +str(meannp)
				coornp = numpy.asarray((z, w))
				#print 'coor:'+ str(coornp)
				dist = numpy.linalg.norm(coornp - meannp)
				#print 'distance ' + str(dist)
				anglerelative = math.degrees(math.atan((z - yMean) / (w - xMean))) - noseAngle
				normalizedFeaturePoints.append(dist)
				normalizedFeaturePoints.append(anglerelative)

		# W przypadku nie znalezienia twarzy zwracamy komunikat bledu
		if len(detections) < 1:
			normalizedFeaturePoints = "No face detected"
		return normalizedFeaturePoints
		
		
	def run(self):
		print 'k'