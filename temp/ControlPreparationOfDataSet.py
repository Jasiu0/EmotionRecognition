import sys
import os
class ControlPreparationOfDataSet():

	# Sprawdzenie bibliotek 
	def checkLibaries(self):
		# Stale
		dlibCheck ='Dlib installed:'
		openCvCheck = 'OpenCv installed:'
		globCheck = 'glob installed:'
		shutilCheck = 'shutil installed:'		
		print "\nChecking libraries"
		
		# OpenCv
		try:
			import cv2
			result = True
		except:
			result = False;
		self.checkResult(openCvCheck,result)
		
		# Dlib	
		try:
			import dlib
			result = True
		except:
			result = False
		self.checkResult(dlibCheck,result)
		
		# Glob	
		try:
			import glob
			result = True
		except:
			result = False
		self.checkResult(dlibCheck,result)
		
		# Copy	
		try:
			from shutil import copy
			result = True
		except:
			result = False
		self.checkResult(dlibCheck,result)
		
	
	# Sprawdzanie przeslanych argumentow
	def checkArguments(self):
		# Stale
		argumentsNumberCheck = 'Number of Arguments:'
		pathToDirectoryWithEmotionTagsCheck = 'Directory With Emotion Tags:'
		pathToDirectoryWithPhotosCheck = 'Directory With Photos:'
		pathToDestinationDirectoryCheck = 'Destination Path:'
		print '\nChecking arguments'
		
		# Sprawdzenie liczby argumentow
		self.checkResult(argumentsNumberCheck,True) if len(sys.argv) == 4 \
		else self.checkResult(argumentsNumberCheck,False)

		# Sprawdzenie istnienia sciezek dostepu
		pathToDirectoryWithEmotionTags = sys.argv[1]
		self.checkResult(pathToDirectoryWithEmotionTagsCheck,True) if(os.path.isdir(pathToDirectoryWithEmotionTags)) \
		else self.checkResult(pathToDirectoryWithEmotionTagsCheck,False)
		
		pathToDirectoryWithPhotosCheck = sys.argv[2]
		self.checkResult(pathToDirectoryWithPhotos,True) if(os.path.isdir(pathToDirectoryWithPhotos)) \
		else self.checkResult(pathToDirectoryWithPhotosCheck,False)
		
		pathToDestinationDirectory = sys.argv[3]
		self.checkResult(pathToDestinationDirectoryCheck,True) if(os.path.isdir(pathToDestinationDirectory)) \
		else self.checkResult(pathToDestinationDirectoryCheck,False)
		
		
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
		
control = ControlPreparationOfDataSet()
control.run()