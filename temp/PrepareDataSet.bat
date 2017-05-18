@echo off
:: Podaj bezwgledna sciezke do folderu z etykietami emocji
SET pathToDirectoryWithEmotionTags=C:\Ck-dataset-emotions\Emotion
:: Podaj bezwgledna sciezke do folder zdjeciami badanych
SET pathToDirectoryWithPhotos=C:\Ck-dataset\cohn-kanade-images
:: Podaj bezwgledna sciezke do folderu do ktorego ma byc zapisany posortowany  zbior
SET pathToDestinationDirectory=C:\organizedDataSet

Python ControlPreparationOfDataSet.py %pathToDirectoryWithEmotionTags% %pathToDirectoryWithPhotos% %pathToDestinationDirectory%