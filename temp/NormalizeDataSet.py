import os
import glob
import cv2
import dlib

class NormalizeDataSet():
	def normalize(self):
		# Zdefiniowanie emocji
		self.emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
		self.savedfiles = 0
		self.counter = [0, 0, 0, 0, 0, 0, 0, 0]
		
		# Sprawdzenie czy uzywane kaskady Haar'a
		if(self.libraryToNormalize == 'OpenCv'):
			self.HaarCascades = []
			for haarCascade in self.HaarCadadeNames:
				# Zapisanie klasyfikatorow Haar'a
				haarCascadeTemp = cv2.CascadeClassifier(self.HaarCascadesDirectory + '\\' + haarCascade + '.xml')
				self.HaarCascades.append(haarCascadeTemp)
		# Sprawdzenie czy uzywane detektor Dlib
		if(self.libraryToNormalize == 'Dlib'):
			self.detector = dlib.get_frontal_face_detector()
		
		self.fileIndex = 0
		# Sprawdza czy sa odpowiednie foldery emocji, jak nie to je tworzy
		for emotion in self.emotions:
			if not os.path.exists(self.pathToNormalizeDirectory + '\\' +emotion):
				os.makedirs(self.pathToNormalizeDirectory + '\\' +emotion)
			files = glob.glob(self.pathToDestinationDirectory + '\\' + emotion + "\\*") 
		

			# Przekonwertuj kazde zdjecie na skale szrosci
			for photo in files:
				frame = cv2.imread(photo)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				if(self.libraryToNormalize == 'OpenCv'):
					self.detectFaceOpenCv(photo, frame, gray, emotion)
				else:
					self.detectFaceDlib(photo, frame, gray, emotion)
		emotionIndex = 0
		for emotion in self.emotions:
			print "Resized " + str(self.counter[emotionIndex]) + " " + emotion + " photos" 
			emotionIndex += 1
		
	def detectFaceOpenCv(self, photo, frame, gray, emotion):
		for HaarCascade in self.HaarCascades:
			face = HaarCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
			if len(face) == 1:
				break;
		file = photo[len(self.pathToDestinationDirectory + '\\' +emotion)+1:-4]
		if len(face) == 0:
			print 'Nie znaleziono twarzy dla pliku: ' + file
		else:
			# Dla twarzy uzysaj punkt zaczepienia oraz szerokosc i wysokosc
			for (xCoordinate, yCoordinate, width, height) in face:
				frame = frame[yCoordinate:yCoordinate + height, xCoordinate:xCoordinate + width]
				self.safeFile(frame, emotion, file)
				
	def detectFaceDlib(self, photo, frame, gray, emotion):
		file = photo[len(self.pathToDestinationDirectory + '\\' +emotion)+1:-4]
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # Zwiekszenie kontrastu
		clahePhoto = clahe.apply(gray)
		# Detekcja za pomoca wbudowanego klasyfikator Dlib
		detections = self.detector(clahePhoto, 1)

		for index,coordinates in  enumerate(detections):
			coordinatesRight = coordinates.right()
			coordinatesLeft = coordinates.left()
			coordinatesTop = coordinates.top()
			coordinatesBottom = coordinates.bottom()
			frame = frame[coordinatesTop:coordinatesBottom, coordinatesLeft:coordinatesRight]
			self.safeFile(frame, emotion, file)
	
	def safeFile(self, frame, emotion, file):
		try:
			# Zmiana wielkosc i szerokosci zdjecia
			resizedFile = cv2.resize(frame, (350, 350))
			# Zapis nowego pliku
			path = self.pathToNormalizeDirectory + '\\' + emotion + '\\' + str(self.fileIndex) + '.jpg'
			#cv2.imwrite(path , resizedFile)
		except:
			print "Error with file saving: " + file
			pass 
		self.fileIndex += 1
		self.counter[self.emotions.index(emotion)] += 1
		
	def run(self, pathToDestinationDirectory, pathToNormalizeDirectory, libraryToNormalize, HaarCascadesDirectory, HaarCadadeNames):
		self.pathToDestinationDirectory = pathToDestinationDirectory
		self.pathToNormalizeDirectory = pathToNormalizeDirectory
		self.libraryToNormalize = libraryToNormalize
		self.HaarCascadesDirectory = HaarCascadesDirectory
		self.HaarCadadeNames = HaarCadadeNames
		print "\nStarting Normalizing DataSet"
		self.normalize()