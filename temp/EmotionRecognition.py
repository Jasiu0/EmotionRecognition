import glob
import cv2
import dlib
import numpy
import math
import time
import threading
from sklearn.svm import SVC

class EmotionRecognition():

	def run(self, programMode, imageSource, imageAcquisitionCycle, predictor, pathToDataSet, \
	classifier, emotions, showImage, showFeaturePoints, outputStream, outputStreamDirectory):
		self.programMode = programMode
		self.imageSource = imageSource
		self.imageAcquisitionCycle = imageAcquisitionCycle
		self.predictor = predictor
		# inicjacja predykatora
		self.shapePredictor = dlib.shape_predictor(self.predictor)
		self.pathToDataSet = pathToDataSet
		self.classifier = classifier
		self.emotions = emotions
		self.showImage = showImage
		self.showFeaturePoints = showFeaturePoints
		self.outputStream = outputStream
		self.outputStreamDirectory = outputStreamDirectory
		# inicjacja detectora dlib
		self.detector = dlib.get_frontal_face_detector()
		self.clf = SVC(kernel=self.classifier, probability=True,tol=1e-3) 
	
		# Uczenie 
		self.train()
		
		if self.programMode == 'fixed':
			self.runFixed()
		
	def runContinuous(self):
		print "cont"
		
	def runFixed(self):

		if self.imageSource == 'camera':
			# Wybor kamery
			self.video_capture = cv2.VideoCapture(0)
			# Petla do predykowania kolejnych zdjec
			while True:	
				image = self.promtPhoto()
				self.getPrediction(image)
				
				
	
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
				# przygotuj obraz do detekcji punktow charakterystycznych
				clahePhoto = self.prepareImage(image)
				# Otrzymaj znormalizowane punkty charakterystyczne
				normalizedFeaturePoints = self.getNormalizedFeaturePoints(clahePhoto)
				if normalizedFeaturePoints == "No face detected":
					print 'No face detected'
					pass
				else:				
					#Dodawanie listy znormalizowanych punktow kontrolnych do zbioru
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
				
		# W przypadku nie znalezienia twarzy zwracamy komunikat bledu
		if len(detections) < 1:
			xList = "No face detected" 
			yList = "No face detected"
		return xList, yList
		
	def getNormalizedFeaturePoints(self, clahePhoto):
		# Otrzymaj punkty charakterystyczne
		xList, yList = self.getFeaturePoints(clahePhoto)
		if xList == "No face detected":
			normalizedFeaturePoints = 'No face detected'
			return normalizedFeaturePoints
		else:
		# Oblicz srodek ciezkosci obrazu dla obu osi
			xMean = numpy.mean(xList)
			yMean = numpy.mean(yList)
			# Oblicz odleglosc pomiedzy punktem a srodkiem ciezkosci dla kazdego z punktow w obu osiach
			xMeanDistance = [(x - xMean) for x in xList]
			yMeanDistance = [(y - yMean) for y in yList]
			# Jezeli punkty w osi x nosa sa w jednej osi kat wynosi 0, w innym przypadku liczymy kat
			if xList[26] == xList[29]:
				noseAngle = 0
			else:
				noseAngle =  math.degrees(math.atan((yList[26] - yList[29]) / (xList[26] - xList[29])))

			if noseAngle < 0:
				noseAngle += 90
			else:
				noseAngle -= 90

			normalizedFeaturePoints = []
			for x,y, w, z in zip(xMeanDistance, yMeanDistance, xList, yList):
				normalizedFeaturePoints.append(x)
				normalizedFeaturePoints.append(y)
				meannp = numpy.asarray((yMean, xMean))
				#print 'mean: ' +str(meannp)
				coornp = numpy.asarray((z, w))
				#print 'coor:'+ str(coornp)
				dist = numpy.linalg.norm(coornp - meannp)
				#print 'distance ' + str(dist)
				if w - xMean != 0:
					anglerelative = math.degrees(math.atan((z - yMean) / (w - xMean))) - noseAngle
				else:
					anglerelative = 0
				normalizedFeaturePoints.append(dist)
				normalizedFeaturePoints.append(anglerelative)
					
		return normalizedFeaturePoints
		
	def train(self):
		print '\nStarting Training'
		trainingData, trainingLabels = self.makeTeachingSet()
		# Tworzenie tablic do klasyfikatora
		npar_train = numpy.array(trainingData)
		npar_trainlabs = numpy.array(trainingLabels)
		# Uczenie
		self.clf.fit(npar_train, trainingLabels)
		print 'Training Finished'
	
	def captureThread(self):
		enter = raw_input("\nClick Enter to acquire photo...")
		self.enter = True
	
	def promtPhoto(self):	
		self.enter = False
		t = threading.Thread(target=self.captureThread)
		t.start()
		
		while self.enter == False:
			ret, image = self.video_capture.read()
			pass
		ret, image = self.video_capture.read()	
		return image
		
	def prepareImage(self, image):
		# Konwersja na skale szarosci
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
		# Zwiekszenie kontrastu
		clahePhoto = clahe.apply(gray)
		return clahePhoto
	
	def predictData(self, normalizedFeaturePoints):
		pred_data = []
		pred_data.append(normalizedFeaturePoints)
		#print pred_data
		im = numpy.array(pred_data)
		pred = self.clf.predict_proba(im)
		#pred = clf.predict(im,0)
		
		for prediction in pred:
			for emotion in self.emotions:
				print str(emotion) + ': ' + str(prediction[self.emotions.index(emotion)])
				
	def getPrediction(self, image):
		clahePhoto = self.prepareImage(image)
		# Otrzymaj znormalizowane punkty charakterystyczne
		normalizedFeaturePoints = self.getNormalizedFeaturePoints(clahePhoto)
		if normalizedFeaturePoints == "No face detected":
			print 'No face detected'
			pass
		else:
			self.predictData(normalizedFeaturePoints)