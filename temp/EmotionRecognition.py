import glob
import cv2
import dlib
import numpy
import math
import time
import datetime
import threading
import os
import ntpath
import random
from sklearn.svm import SVC

class EmotionRecognition():

	def run(self, programMode, imageSource, imageAcquisitionCycle, predictor, pathToDataSet, \
	classifier, emotions, showImage, showFeaturePoints, outputStream, outputStreamDirectory):
		self.programMode = programMode
		self.imageSource = imageSource
		if self.programMode == 'continuous':
			self.imageAcquisitionCycle = int(imageAcquisitionCycle)
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
		if programMode != 'research':
			self.train()
		else:
			self.runResearch()
		
		if self.programMode == 'fixed':
			self.runFixed()
		elif self.programMode == 'continuous':	
			self.runContinuous()
		
	def runContinuous(self):
		if self.outputStream =='file':
				timeStamp = self.getDataTime()
				if os.path.exists(self.outputStreamDirectory):
					directory = self.outputStreamDirectory + '\\' + timeStamp
					os.makedirs(directory)
					fileName = directory + '\\' + timeStamp + '.txt'
					file = open(fileName,'w') 
					file.close()
					with open(fileName, "a") as myfile:
						myfile.write('|'.join(self.emotions)+'\n')
		self.video_capture = cv2.VideoCapture(0)
		if(self.showImage == 'True'):
			threadShowCamera = threading.Thread(target=self.showCamera)
			threadShowCamera.start()
		while True:	
				image = self.promtFrame()
				emotionsToFile = self.getPredictionFrom(image)
				if(self.outputStream =='file'):
					with open(fileName, "a") as myfile:
						myfile.write(emotionsToFile)
				timeStamp = self.getDataTime()		
				cv2.imwrite(directory + '\\' + timeStamp + ".jpg", image)		
		
	def runFixed(self):

		# Utworzenie pliku z logowaniem jezeli tak wybrano
		if self.outputStream =='file':
				timeStamp = self.getDataTime()
				if os.path.exists(self.outputStreamDirectory):
					directory = self.outputStreamDirectory + '\\' + timeStamp
					os.makedirs(directory)
					fileName = directory + '\\' + timeStamp + '.txt'
					file = open(fileName,'w') 
					file.close()
					with open(fileName, "a") as myfile:
						myfile.write('|'.join(self.emotions)+'\n')
		if self.imageSource == 'camera':
			# Wybor kamery
			self.video_capture = cv2.VideoCapture(0)
			if(self.showImage == 'True'):
				threadShowCamera = threading.Thread(target=self.showCamera)
				threadShowCamera.start()

			# Petla do predykowania kolejnych zdjec
			while True:	
				image = self.promtPhoto()
				emotionsToFile = self.getPredictionFrom(image)
				if(self.outputStream =='file'):
					with open(fileName, "a") as myfile:
						myfile.write(emotionsToFile)
				timeStamp = self.getDataTime()		
				cv2.imwrite(directory + '\\' + timeStamp + ".jpg", image)	
		
		elif self.imageSource == 'file':
			# Petla do predykowania kolejnych zdjec
			while True:	
				image = self.promtFile()
				emotionsToFile = self.getPredictionFrom(image)
				if(self.outputStream =='file'):
					with open(fileName, "a") as myfile:
						myfile.write(emotionsToFile)
						
		elif self.imageSource == 'directory':
			# Petla do predykowania kolejnych zdjec
			while True:	
				directory = self.promtDirectory()
				files = glob.glob(directory + "\\*") 
				for self.filePath in files:
					if self.filePath.lower().endswith(('.png', '.jpg', '.jpeg')):
						image = cv2.imread(self.filePath)
						emotionsToFile = self.getPredictionFrom(image)
						if(self.outputStream =='file'):
							with open(fileName, "a") as myfile:
								myfile.write(emotionsToFile)						
			
	def runResearch(self):
		# Dokladnosc
		accuracy = []
		# Aby dac obiektywne wyniki wykonaj badanie 5 razy przy roznych podzialach
		for i in range(0, 5):
			trainingData, trainingLabels, predictionData, predictionLabels = self.makeResearchSet()
			# Tworzenie tablic do klasyfikatora
			numpyTrainArrayData = numpy.array(trainingData)
			numpyTrainArrayLabels = numpy.array(trainingLabels)
			print('\nTraining SVM') #train SVM
			# Uczenie
			self.clf.fit(numpyTrainArrayData, numpyTrainArrayLabels)

			print('Calculating Accuracy')
			numpyPredictionArrayData = numpy.array(predictionData)
			testAccuracy = self.clf.score(numpyPredictionArrayData, predictionLabels)
			print "Accuracy: " + str(testAccuracy)
			#Zapisz wynik do tablicy
			accuracy.append(testAccuracy)
		print "\nMean Accuracy: " + str(numpy.mean(accuracy))
		
	def divideData(self, emotion):
		files = glob.glob(self.pathToDataSet + '\\' +  emotion+ '\\*')
		random.shuffle(files)
		# Podzial w stosunku 8:2 na zbior do uczenia i testowania
		trainingDataSet = files[:int(len(files) * 0.8)]
		predictionDataSet = files[-int(len(files) * 0.2):]
		return trainingDataSet, predictionDataSet
	
	def showCamera(self):
		while True:
			ret, image = self.video_capture.read()	
			if self.showFeaturePoints == 'True':
				self.getFeaturePoints(image)
			cv2.imshow("image", image)
			cv2.waitKey(60)
		
	def makeTeachingSet(self):
		trainingData = []
		trainingLabels = []
		for emotion in self.emotions:
			print '\nTraining ' + emotion + ' emotion'
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
					fileName = file[len(self.pathToDataSet)+len(emotion)+2:]
					print 'Training ' + fileName + ' file finished'
			print 'Training ' + emotion + ' emotion finished'

		return trainingData, trainingLabels

	def makeResearchSet(self):
		trainingData = []
		trainingLabels = []
		predictionData = []
		predictionLabels = []
		for emotion in self.emotions:
			print '\nTraining ' + emotion + ' emotion'
			trainingDataSet, predictionDataSet = self.divideData(emotion)
			# Dla kazdego obrazu w zbiorze uczacym
			for file in trainingDataSet:
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
					fileName = file[len(self.pathToDataSet)+len(emotion)+2:]
					print 'Training ' + fileName + ' file finished'
			print 'Training ' + emotion + ' emotion finished'
			
			print '\nPredicting ' + emotion + ' emotion'
			for file in predictionDataSet:
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
					predictionData.append(normalizedFeaturePoints)
					predictionLabels.append(self.emotions.index(emotion))
					fileName = file[len(self.pathToDataSet)+len(emotion)+2:]
					print 'Predicting ' + fileName + ' file finished'
			print 'Prediction ' + emotion + ' emotion finished'

		return trainingData, trainingLabels, predictionData, predictionLabels

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
				if(self.showFeaturePoints == 'True'):
					cv2.circle(photo, (shape.part(featurePoint).x, shape.part(featurePoint).y), 1, (0, 0, 255),thickness=2)
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
			for xMeanValue,yMeanValue, xElement, yElement in zip(xMeanDistance, yMeanDistance, xList, yList):
				normalizedFeaturePoints.append(xMeanValue)
				normalizedFeaturePoints.append(yMeanValue)
				numpyMeanArray = numpy.asarray((yMean, xMean))
				numpyElementArray = numpy.asarray((yElement, xElement))
				dist = numpy.linalg.norm(numpyElementArray - numpyMeanArray)
				if xElement - xMean != 0:
					anglerelative = math.degrees(math.atan((yElement - yMean) / (xElement - xMean))) - noseAngle
				else:
					anglerelative = 0
				normalizedFeaturePoints.append(dist)
				normalizedFeaturePoints.append(anglerelative)
					
		return normalizedFeaturePoints
		
	def train(self):
		print '\nStarting Training'
		trainingData, trainingLabels = self.makeTeachingSet()
		# Tworzenie tablic do klasyfikatora
		numpyTrainArrayData = numpy.array(trainingData)
		numpyTrainArrayLabels = numpy.array(trainingLabels)
		# Uczenie
		self.clf.fit(numpyTrainArrayData, numpyTrainArrayLabels)
		print 'Training Finished'
	
	def captureThread(self):
		enter = raw_input("\nClick Enter to acquire photo...")
		self.enter = True
	
	def captureFrameThread(self):
		start = time.time()
		time.clock()    
		elapsed = 0

		while int(elapsed) < self.imageAcquisitionCycle:
			elapsed = time.time() - start
			#print elapsed 
			time.sleep(1)  

		self.threadTime = True	
		
	def captureFilePathThread(self):
		self.filePath = raw_input("\nPlease input path to file...")
		
	def captureDirectoryPathThread(self):
		self.fileDirectory = raw_input("\nPlease input path to file...")	
				
	def promtPhoto(self):	
		self.enter = False
		threadPhoto = threading.Thread(target=self.captureThread)
		threadPhoto.start()
		
		while self.enter == False:
			ret, image = self.video_capture.read()
			pass
		ret, image = self.video_capture.read()	
		return image
	
	def promtFrame(self):	
		self.threadTime = False
		threadFrame = threading.Thread(target=self.captureFrameThread)
		threadFrame.start()
		
		while self.threadTime == False:
			ret, image = self.video_capture.read()
			pass
		ret, image = self.video_capture.read()	
		return image	
	
	def promtFile(self):
		self.filePath = ' '
		threadPhoto = threading.Thread(target=self.captureFilePathThread)
		threadPhoto.start()
		
		while self.filePath == ' ':
			pass
		if os.path.isfile(self.filePath):
			image = cv2.imread(self.filePath)
			return image
		else: 
			print '\nFile not found'
			image = self.promtFile()
			return image
			
	def promtDirectory(self):
		self.fileDirectory = ' '
		threadDirectory = threading.Thread(target=self.captureDirectoryPathThread)
		threadDirectory.start()
		
		while self.fileDirectory == ' ':
			pass
		if os.path.isdir(self.fileDirectory):
			return self.fileDirectory
		else: 
			print '\nDirectory not found'
			directory = self.promtDirectory()
		return directory	
		
	def prepareImage(self, image):
		# Konwersja na skale szarosci
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
		# Zwiekszenie kontrastu
		clahePhoto = clahe.apply(gray)
		return clahePhoto
	
	def predictDataFrom(self, normalizedFeaturePoints):
		predictionData = []
		predictionData.append(normalizedFeaturePoints)
		image = numpy.array(predictionData)
		predictionList = self.clf.predict_proba(image)
		if self.imageSource == 'camera' or self.programMode == 'continuous':
			timeStamp = self.getDataTime()
			emotionsToFile = timeStamp + '|'
		else: 
			head, fileName = ntpath.split(self.filePath)
			emotionsToFile =  fileName + '|'
		for prediction in predictionList:
			for emotion in self.emotions:
				print str(emotion) + ': ' + str(prediction[self.emotions.index(emotion)])
				emotionsToFile += str(prediction[self.emotions.index(emotion)]) +'|'
		emotionsToFile+='\n'		
		return emotionsToFile
				
	def getPredictionFrom(self, image):
		clahePhoto = self.prepareImage(image)
		# Otrzymaj znormalizowane punkty charakterystyczne
		normalizedFeaturePoints = self.getNormalizedFeaturePoints(clahePhoto)
		if normalizedFeaturePoints == "No face detected":
			print 'No face detected'
			return ''
		else:
			emotionsToFile = self.predictDataFrom(normalizedFeaturePoints)
			return emotionsToFile
			
	def getDataTime(self):
		timeInSeconds = time.time()
		timeStamp = datetime.datetime.fromtimestamp(timeInSeconds).strftime('%Y-%m-%d %H.%M.%S')
		return timeStamp			