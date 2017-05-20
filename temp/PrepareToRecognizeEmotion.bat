@echo off
:: Wybor trybu dzialania [continuous, fixed] 
SET programMode=fixed
:: Wybor zrodla obrazu [camera, file, directory]
SET imageSource=camera
:: Podaj bezwgledna sciezke do predykatora Dlib
SET predictor=C:\EmotionRecognition\temp\shape_predictor_68_face_landmarks.dat
:: Podaj bezwgledna sciezke do zbioru uczacego
SET pathToDirectoryWithPhotos=C:\cutDataSet
:: Wybierz klasyfikator [linear,...]
SET classifier=linear
:: Wybor emocji ["anger", "contempt", "disgust", "fear", "happy", "neutral", "sadness", "surprise"]
SET emotions=["anger", "contempt", "disgust", "fear", "happy", "neutral", "sadness", "surprise"]
:: Wyswietlanie obrazu [True, False]
SET showImage=True
:: Wyswietlanie znacznikow [True, False] ( dziala w przypadku wybrania wyswietlania obrazu)
SET showFeaturePoints=True
:: Wybor strumienia wyjscia [console, file]
SET outputStream=console


:: Sprawdzenie istnienia zainstalowanego pythona
echo.
echo Checking Python Module
python --version 2>NUL
if errorlevel 1 echo Python installed:                 Fail && exit /b
echo Python installed:               Pass

Python EmotionRecognitionValidation.py %1 %programMode% %imageSource% %predictor% %pathToDirectoryWithPhotos% ^
%classifier% %emotions% %showImage% %showFeaturePoints% %outputStream%
echo.
pause