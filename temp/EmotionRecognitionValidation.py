import sys
import os

class EmotionRecognitionValidation():

	def checkArguments(self):
		# Stale
		argumentsNumberCheck = 'Number of Arguments:'
		programModeCheck = 'Program mode:'
		
		# Sprawdzenie liczby argumentow
		print len(sys.argv)
		self.checkResult(argumentsNumberCheck,True) if len(sys.argv) == 9 \
		else self.checkResult(argumentsNumberCheck,False)
		
		self.programMode = sys.argv[1]
		self.checkResult(programModeCheck,True) if self.programMode in ['continuous', 'fixed']  \
		else self.checkResult(programModeCheck,False)
	
	
	
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
		#self.checkClasses()
		
EmotionRecognitionValidationController = EmotionRecognitionValidation()
EmotionRecognitionValidationController.run()