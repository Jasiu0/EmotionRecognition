import sys
import os

# Rozpoczecie testow
print "\nChecking arguments"

# Sprawdzenie liczby argumentow
if len(sys.argv) != 4:
    sys.exit('Number of Arguments: Fail!')
print 'Number of Arguments: Pass'

# Sprawdzenie istnienia sciezek dostepu
pathToDirectoryWithEmotionTags = sys.argv[1]
print pathToDirectoryWithEmotionTags
if not(os.path.isdir(pathToDirectoryWithEmotionTags)):
	sys.exit('Directory With Emotion Tags: Fail!')
print 'Directory With Emotion Tags: Pass'
pathToDirectoryWithPhotos = sys.argv[2]
if not(os.path.isdir(pathToDirectoryWithPhotos)):
	sys.exit('Directory With Photos: Fail!')
print 'Directory With Photos: Pass'
pathToDestinationDirectory = sys.argv[3]
if not(os.path.isdir(pathToDirectoryWithEmotionTags)):
	sys.exit('Directory With Emotion Tags: Fail!')
print 'Directory With Emotion Tags: Pass'
	
print "\nChecking libraries"