import glob
import cv2
import dlib
import numpy

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
		
		print '\nStarting Training'
		trainingData, trainingLabels = self.makeTeachingSet()
		print 'Training Finished'
		
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
				if normalizedFeaturePoints == "error":
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
			xCentral = [(x - xMean) for x in xList]
			yCentral = [(y - yMean) for y in yList]

			#if xlist[26] == xlist[
		#		29]:  # If x-coordinates of the set are the same, the angle is 0, catch to prevent 'divide by 0' error in function
		#		anglenose = 0
		#	else:
		#		anglenose = int(math.atan((ylist[26] - ylist[29]) / (xlist[26] - xlist[29])) * 180 / math.pi)
#
#			if anglenose < 0:
#				anglenose += 90
#			else:
#				anglenose -= 90
#
#			landmarks_vectorised = []
#			for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
#				landmarks_vectorised.append(x)
#				landmarks_vectorised.append(y)
#				meannp = np.asarray((ymean, xmean))
#				coornp = np.asarray((z, w))
#				dist = np.linalg.norm(coornp - meannp)
#				anglerelative = (math.atan((z - ymean) / (w - xmean)) * 180 / math.pi) - anglenose
#				landmarks_vectorised.append(dist)
#				landmarks_vectorised.append(anglerelative)

#		if len(detections) < 1:
#			landmarks_vectorised = "error"
		landmarks_vectorised =[]
		return landmarks_vectorised
		
		
	def run(self):
		print 'k'