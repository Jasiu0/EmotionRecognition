import glob
from shutil import copy
import os

class OrganizeDataSet():
	def organize(self):

		# Zdefiniowanie emocji
		emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
		# Licznik kopiowanych plikow
		counter = [0, 0, 0, 0, 0, 0, 0, 0]

		# Sprawdza czy sa odpowiednie foldery emocji, jak nie to je tworzy
		for emotion in emotions:
			if not os.path.exists(self.pathToDestinationDirectory + '\\' +emotion):
				os.makedirs(self.pathToDestinationDirectory + '\\' +emotion)
		
		#  Zwraca liste uczestnikow
		participants = glob.glob(self.pathToDirectoryWithEmotionTags + "\\*")

		# Dla kazdego uczestnika
		for participant in participants:
			# Dla kazdej emocji
			for participantEmotions in glob.glob(participant + "\\*"):
				# Dla Plikow w folderze z emocjami
				for files in glob.glob(participantEmotions + "\\*"):
					# Zwraca obecna sciezke bez path
					folder = files[len(self.pathToDirectoryWithEmotionTags)+1:-30]
					# tworz plik txt
					file = open(files, 'r')
					# odczytanie emocji
					emotion = int(float(file.readline()))
					# sciezka do ostatniego zdjecia w danym folderze (skrajna emocja)
					sourceEmotion = glob.glob(self.pathToDirectoryWithPhotos + "\\" + folder + "\\*")[-1]
					# sciezka do pierwszego zdjecia w danym folderze (neutralna emocja)
					sourceNeutral = glob.glob(self.pathToDirectoryWithPhotos + "\\" + folder + "\\*")[0]  # do same for neutral image
					# sciezka do kopiowania danego pliku z naturalna emocja
					destinationNeutral = self.pathToDestinationDirectory + "\\neutral"
					# sciezka do kopiowania danego pliku z skrajna emocja
					destinationEmotion = self.pathToDestinationDirectory + "\\" + emotions[emotion]
					# kopiowanie plikow
					#copy(sourceNeutral, destinationNeutral)
					#copy(sourceEmotion, destinationEmotion)
					counter[0] += 1
					counter[emotion] += 1
		emotionIndex = 0
		for emotion in emotions:
			print "Copied " + str(counter[emotionIndex]) + " " + emotion + " photos" 
			emotionIndex += 1
		
					
	def run(self, pathToDirectoryWithEmotionTags, pathToDirectoryWithPhotos, pathToDestinationDirectory):
		self.pathToDirectoryWithEmotionTags = pathToDirectoryWithEmotionTags
		self.pathToDirectoryWithPhotos = pathToDirectoryWithPhotos
		self.pathToDestinationDirectory = pathToDestinationDirectory
		print "\nStarting Organizing DataSet"
		self.organize()
		
