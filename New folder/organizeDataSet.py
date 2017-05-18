import glob
from shutil import copy

# Sciezka do zbioru z badanymi emocjami, zdjeciami i docelowa
pathEmotions = "C:\Ck-dataset-emotions\Emotion"
pathPhotos = "C:\Ck-dataset\cohn-kanade-images"
pathDestination = "C:\organizedDataSet"

# Zdefiniowanie emocji
emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
#  Zwraca liste uczestnikow
participants = glob.glob(pathEmotions + "\\*")

# Dla kazdego uczestnika
for participant in participants:
    # Dla kazdej emocji
    for participantEmotions in glob.glob(participant + "\\*"):
        # Dla Plikow w folderze z emocjami
        for files in glob.glob(participantEmotions + "\\*"):
            # Zwraca obecna sciezke bez path
            folder = files[len(pathEmotions)+1:-30]
            # tworz plik txt
            file = open(files, 'r')
            # odczytanie emocji
            emotion = int(float(file.readline()))
            # sciezka do ostatniego zdjecia w danym folderze (skrajna emocja)
            sourceEmotion = glob.glob(pathPhotos + "\\" + folder + "\\*")[-1]
            # sciezka do pierwszego zdjecia w danym folderze (neutralna emocja)
            sourceNeutral = glob.glob(pathPhotos + "\\" + folder + "\\*")[0]  # do same for neutral image
            # sciezka do kopiowania danego pliku z naturalna emocja
            destinationNeutral = pathDestination + "\\neutral"
            # sciezka do kopiowania danego pliku z skrajna emocja
            destinationEmotion = pathDestination + "\\" + emotions[emotion]
            # kopiowanie plikow
            copy(sourceNeutral, destinationNeutral)
            copy(sourceEmotion, destinationEmotion)

