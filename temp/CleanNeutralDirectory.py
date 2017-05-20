import glob
import os

class CleanNeutralDirectory():
	def cleaning(self):
		#  Zwraca liste uczestnikow
		participants = glob.glob(self.pathToNeutralDirectory + "\\*")
		# Tymczasowa zmienna przechowujaca ostatni index badanego
		last = ''
		# Licznik usunietych plikow
		counter = 0
		# Dla kazdego obrazu
		for participant in participants:
			participantIndex = participant[len(self.pathToNeutralDirectory)+1:-17]
			# Jezeli index badanego rozny nadpisz, inaczej usun plik
			if last != participantIndex:
				last =  participant[len(self.pathToNeutralDirectory)+1:-17]
			else:
				# Usun plik
				os.remove(participant) 
				counter += 1
		print 'Deleted ' + str(counter) + ' files'
				
	def run(self, pathToNeutralDirectory):
		self.pathToNeutralDirectory = pathToNeutralDirectory
		print "\nStarting Cleaning Neutral Directory"
		self.cleaning()
		
