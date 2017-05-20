@echo off
:: Podaj bezwgledna sciezke do folderu z etykietami emocji
SET pathToDirectoryWithEmotionTags=C:\Ck-dataset-emotions\Emotion
:: Podaj bezwgledna sciezke do folder zdjeciami badanych
SET pathToDirectoryWithPhotos=C:\Ck-dataset\cohn-kanade-images
:: Podaj bezwgledna sciezke do folderu do ktorego ma byc zapisany posortowany  zbior
SET pathToDestinationDirectory=C:\organizedDataSet
:: Wybor czyszczenia neutralnego folderu z wielu zdjec dla tego samego uzytkownika [Tak - 1, Nie - 0]
SET cleaningDirectory=True
:: Podaj bezwgledna sciezke do folder do ktorego maja zostac zapisane znormalizowane zdjecia
SET pathToNormalizeDirectory=C:\EmotionRecognition\temp\check
:: Wybierz bilbiotek do normalizacji [OpenCv, Dlib] 
SET libraryToNormalizeWith=OpenCv
:: Podaj bezwgledna sciezke do folderu z kaskadami Haar'a ( W przypadku uzycia biblioteki Dlib wpisz -)
::(haarcascade_frontalface_default, haarcascade_frontalface_alt2, haarcascade_frontalface_alt, haarcascade_frontalface_alt_tree)
SET pathToHaarCascadeDirectory=C:\OpenCV\opencv\sources\data\haarcascades


:: Sprawdzenie istnienia zainstalowanego pythona
echo.
echo Checking Python Module
python --version 2>NUL
if errorlevel 1 echo Python installed:                 Fail && exit /b
echo Python installed:               Pass

Python PrepareToCreateDataSet.py %pathToDirectoryWithEmotionTags% %pathToDirectoryWithPhotos% %pathToDestinationDirectory% %cleaningDirectory% ^
%pathToNormalizeDirectory% %libraryToNormalizeWith% %pathToHaarCascadeDirectory%
echo.
pause