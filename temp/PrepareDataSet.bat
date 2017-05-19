@echo off
:: Podaj bezwgledna sciezke do folderu z etykietami emocji
SET pathToDirectoryWithEmotionTags=C:\Ck-dataset-emotions\Emotion
:: Podaj bezwgledna sciezke do folder zdjeciami badanych
SET pathToDirectoryWithPhotos=C:\Ck-dataset\cohn-kanade-images
:: Podaj bezwgledna sciezke do folderu do ktorego ma byc zapisany posortowany  zbior
SET pathToDestinationDirectory=C:\organizedDataSet

:: Sprawdzenie istnienia zainstalowanego pythona
echo.
echo Checking Python Module
python --version 2>NUL
if errorlevel 1 echo Python installed:                 Fail && exit /b
echo Python installed:               Pass

Python PrepareToCreateDataSet.py %pathToDirectoryWithEmotionTags% %pathToDirectoryWithPhotos% %pathToDestinationDirectory%
