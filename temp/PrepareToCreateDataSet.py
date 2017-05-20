import sys
import os
class PrepareToCreateDataSet():

	# Sprawdzenie bibliotek 
	def checkLibaries(self):
		# Stale
		dlibCheck ='dlib installed:'
		openCvCheck = 'Cv2 installed:'
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
		self.checkResult(globCheck,result)
		
		# Copy	
		try:
			from shutil import copy
			result = True
		except:
			result = False
		self.checkResult(shutilCheck,result)
		
	
	# Sprawdzanie przeslanych argumentow
	def checkArguments(self):
		# Stale
		argumentsNumberCheck = 'Number of Arguments:'
		pathToDirectoryWithEmotionTagsCheck = 'Directory With Emotion Tags:'
		pathToDirectoryWithPhotosCheck = 'Directory With Photos:'
		pathToDestinationDirectoryCheck = 'Destination to Organize:'
		cleaningDirectoryCheck = 'Cleaning Directory:'
		pathToNormalizeDirectoryCheck = 'Destinantion to Normalize'
		LibraryToNormalizeCheck = 'Library to Normalize with'
		HaarCascadeCheck = 'Directory with Haar Cascades:'
		HaarCadadeNames = ['haarcascade_frontalface_default', 'haarcascade_frontalface_alt2', \
		'haarcascade_frontalface_alt', 'haarcascade_frontalface_alt_tree']
		print '\nChecking arguments'
		
		# Sprawdzenie liczby argumentow
		self.checkResult(argumentsNumberCheck,True) if len(sys.argv) == 8 \
		else self.checkResult(argumentsNumberCheck,False)

		# Sprawdzenie istnienia sciezek dostepu
		self.pathToDirectoryWithEmotionTags = sys.argv[1]
		self.checkResult(pathToDirectoryWithEmotionTagsCheck,True) if(os.path.isdir(self.pathToDirectoryWithEmotionTags)) \
		else self.checkResult(pathToDirectoryWithEmotionTagsCheck,False)
		
		self.pathToDirectoryWithPhotos = sys.argv[2]
		self.checkResult(pathToDirectoryWithPhotosCheck,True) if(os.path.isdir(self.pathToDirectoryWithPhotos)) \
		else self.checkResult(pathToDirectoryWithPhotosCheck,False)
		
		self.pathToDestinationDirectory = sys.argv[3]
		self.checkResult(pathToDestinationDirectoryCheck,True) if(os.path.isdir(self.pathToDestinationDirectory)) \
		else self.checkResult(pathToDestinationDirectoryCheck,False)
		
		# Sprawdzenie poprawnego wyboru czyszczenia
		self.cleaningDirectory = sys.argv[4]
		self.checkResult(cleaningDirectoryCheck,True) if(self.cleaningDirectory in ['True', 'False']) \
		else self.checkResult(cleaningDirectoryCheck,False)
		
		# Sprawdzanie istnienia sciezki dostepu do zapisania znormalizowanego zbioru
		self.pathToNormalizeDirectory = sys.argv[5]
		self.checkResult(pathToDestinationDirectoryCheck,True) if(os.path.isdir(self.pathToNormalizeDirectory)) \
		else self.checkResult(pathToDestinationDirectoryCheck,False)
		
		# Sprawdzenie poprawnego wyboru biblioteki
		self.libraryToNormalize = sys.argv[6]
		self.checkResult(LibraryToNormalizeCheck,True) if(self.libraryToNormalize in ['OpenCv', 'Dlib']) \
		else self.checkResult(LibraryToNormalizeCheck,False)
		
		if(self.libraryToNormalize == 'OpenCv'):
			# Sprawdzenie dostepu do kaskad Haar'a
			checkHaarCasade = True
			self.HaarCascadesDirectory = sys.argv[7]
			for haarCascade in HaarCadadeNames:
				if not os.path.isfile(self.HaarCascadesDirectory + '\\' + haarCascade + '.xml'):
					checkHaarCasade = False
			self.checkResult(HaarCascadeCheck,True) if(checkHaarCasade == True) \
			else self.checkResult(HaarCascadeCheck,False)
		else: 
			self.HaarCascadesDirectory =''

		
	def checkClasses(self):	
		OrganizeDataSetClass = 'Organize Data Set Class:'
		CleanNeutralDirectoryClass = 'Clean Neutral Directory Class:'
		NormalizeDataSetClass = 'Normalize Data Set Class'
		print '\nChecking Classes'
		# Organize Data Set Class	
		try:
			from OrganizeDataSet import OrganizeDataSet
			result = True
		except:
			result = False
		self.checkResult(OrganizeDataSetClass,result)
		
		# Clean Neutral Directory Class	
		try:
			from CleanNeutralDirectory import CleanNeutralDirectory
			result = True
		except:
			result = False
		self.checkResult(CleanNeutralDirectoryClass,result)
		
		# Normalize Data Set Class	
		try:
			from NormalizeDataSet import NormalizeDataSet
			result = True
		except:
			result = False
		self.checkResult(NormalizeDataSetClass,result)

		
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
		self.checkLibaries()
		self.checkArguments()
		self.checkClasses()
		from OrganizeDataSet import OrganizeDataSet
		organizeDataSetController = OrganizeDataSet()
		organizeDataSetController.run(self.pathToDirectoryWithEmotionTags, self.pathToDirectoryWithPhotos, self.pathToDestinationDirectory)
		from CleanNeutralDirectory import CleanNeutralDirectory
		cleanNeutralDirectoryController = CleanNeutralDirectory()
		cleanNeutralDirectoryController.run(self.pathToDestinationDirectory+ "\\neutral")
		from NormalizeDataSet import NormalizeDataSet
		normalizeDataSetController = NormalizeDataSet()
		normalizeDataSetController.run()
		
prepareDataSetController = PrepareToCreateDataSet()
prepareDataSetController.run()