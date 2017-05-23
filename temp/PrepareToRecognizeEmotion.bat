@echo off
:: Wybor trybu dzialania [continuous, fixed, research] 
SET programMode=fixed
:: Wybor zrodla obrazu [camera, file, directory]
SET imageSource=camera
:: Czas pomiedzy pobieraniem ramek (int) Brane pod uwage tylko przy wyborze zrodla obrazu z kamery
SET imageAcquisitionCycle=10
:: Podaj bezwgledna sciezke do predykatora Dlib
SET predictor=C:\EmotionRecognition\temp\shape_predictor_68_face_landmarks.dat
:: Podaj bezwgledna sciezke do zbioru uczacego
SET pathToDataSet=C:\cutDataSet
:: Wybierz klasyfikator [linear, polynomial, rbf]
SET classifier=linear
:: Wybor emocji ["anger", "contempt", "disgust", "fear", "happy", "neutral", "sadness", "surprise"]
::SET emotions=[\"anger\",\"contempt\",\"disgust\",\"fear\",\"happy\",\"neutral\",\"sadness\",\"surprise\"]
SET emotions=[\"happy\",\"neutral\"]
:: Wyswietlanie obrazu [True, False]
SET showImage=True
:: Wyswietlanie znacznikow [True, False] ( dziala w przypadku wybrania wyswietlania obrazu)
SET showFeaturePoints=True
:: Wybor strumienia wyjscia [console, file]
SET outputStream=console
:: Wybor sciezki do pliku ze strumienia wyjscia
SET outputStreamDirectory=C:\EmotionRecognition\temp

:: Sprawdzenie istnienia zainstalowanego pythona
echo.
echo Checking Python Module
python --version 2>NUL
if errorlevel 1 echo Python installed:                 Fail && exit /b
echo Python installed:               Pass

Python EmotionRecognitionValidation.py %programMode% %imageSource% %imageAcquisitionCycle% %predictor% ^
%pathToDataSet% %classifier% %emotions% %showImage% %showFeaturePoints% %outputStream% %outputStreamDirectory%
echo.
pause