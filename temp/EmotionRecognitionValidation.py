import sys
import os

class EmotionRecognitionValidation():

	def checkArguments(self):
		# Stale
		argumentsNumberCheck = 'Number of Arguments:'
		programModeCheck = 'Program mode:'
		imageSourceCheck = 'Image Source:'
		imageAcquisitionCycleCheck = 'Image Acquisition Cycle:'
		predictorCheck = 'Precidtor:'
		pathToDataSetCheck = 'Path To Data Set'
		classifierCheck = 'Classifier:'
		emotionsCheck = 'Emotions:'
		showImageCheck = 'View mode:'
		showFeaturePointsCheck = 'Feature Points Visibility:'
		outputStreamCheck = 'Output Stream:'
		outputStreamDirectoryCheck = 'Output Stream Directory:'
		
		print '\nChecking arguments'
		# Sprawdzenie liczby argumentow
		self.checkResult(argumentsNumberCheck,True) if len(sys.argv) == 12 \
		else self.checkResult(argumentsNumberCheck,False)
		
		# Sprawdzenie poprawnego wyboru trybu modulu
		self.programMode = sys.argv[1]
		self.checkResult(programModeCheck,True) if self.programMode in ['continuous', 'fixed', 'research']  \
		else self.checkResult(programModeCheck,False)
	
		# Sprawdzenie poprawnego wyboru strumienia wejsciowego
		self.imageSource = sys.argv[2]
		self.checkResult(imageSourceCheck,True) if self.imageSource in ['camera', 'file', 'directory']  \
		else self.checkResult(imageSourceCheck,False)
		
		
		# Sprawdzenie poprawnego odstepu pomiedzy pobieraniem ramek
		if(self.imageSource == 'camera'):
			self.sourcePeriod = sys.argv[3]
			self.checkResult(imageAcquisitionCycleCheck,True) if self.sourcePeriod.isdigit()  \
			else self.checkResult(imageAcquisitionCycleCheck,False)

		# Sprawdzenie istnienia predykatora
		self.predictor = sys.argv[4]
		self.checkResult(predictorCheck,True) if os.path.isfile(self.predictor) \
		else self.checkResult(predictorCheck,False)
		
		# Sprawdzenie dostepu do zbioru danych
		self.pathToDataSet = sys.argv[5]
		self.checkResult(pathToDataSetCheck,True) if os.path.isdir(self.pathToDataSet) \
		else self.checkResult(pathToDataSetCheck,False)
		
		# Sprawdzenie poprawnego wyboru klasyfikatora
		self.classifier = sys.argv[6]
		self.checkResult(classifierCheck,True) if self.classifier in ['linear', 'polynomial', 'rbf'] \
		else self.checkResult(classifierCheck,False)
		
		# Sprawdzenie poprawnosci emocji
		self.emotions = eval(sys.argv[7])
		for emotion in self.emotions:
			if not emotion in ['anger', 'contempt', 'disgust', 'fear', 'happy', 'neutral', 'sadness', 'surprise']:
				self.checkResult(emotionsCheck,False)
		self.checkResult(emotionsCheck,True)
		
		# Sprawdzenie poprawnosci wyboru wyswietlenia obrazu
		self.showImage = sys.argv[8]
		self.checkResult(showImageCheck,True) if(self.showImage in ['True', 'False']) \
		else self.checkResult(showImageCheck,False)
		
		self.showFeaturePoints = sys.argv[9]
		if self.showImage == 'True':
			self.checkResult(showFeaturePointsCheck,True) if(self.showFeaturePoints in ['True', 'False']) \
			else self.checkResult(showFeaturePointsCheck,False)
			
		self.outputStream = sys.argv[10]
		self.checkResult(outputStreamCheck,True) if(self.outputStream in ['console', 'file']) \
		else self.checkResult(outputStreamCheck,False)
		
		self.outputStreamDirectory = sys.argv[11]
		self.checkResult(outputStreamDirectoryCheck,True) if os.path.isdir(self.outputStreamDirectory) \
		else self.checkResult(outputStreamDirectoryCheck,False)
		
	def checkClasses(self):	
		EmotionRecognitionClass = 'Emotion Recognition Class:'

		print '\nChecking Classes'
		# Emotion Recognition Class
		try:
			from EmotionRecognition import EmotionRecognition
			result = True
		except:
			result = False
		self.checkResult(EmotionRecognitionClass, result)	
		
	# Wyswietlanie wyniku testu	
	def checkResult(self, testName, flag):
		length = 35
		resultFormatting = '%s %'+ str(length - len(testName)) + 's'
		if flag == True:
			result = 'Pass'	
			print resultFormatting % (testName,result)	
		else:
			result = 'Fail'
			sys.exit(resultFormatting % (testName,result))

	def run(self):
		# Testy
		#self.checkLibaries()
		self.checkArguments()
		self.checkClasses()
		
		# Rozpoznawanie emocji
		from EmotionRecognition import EmotionRecognition
		EmotionRecognitionController = EmotionRecognition()
		EmotionRecognitionController.run()
		
EmotionRecognitionValidationController = EmotionRecognitionValidation()
EmotionRecognitionValidationController.run()