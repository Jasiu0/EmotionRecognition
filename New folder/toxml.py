__author__ = 'Jasiu'
import cv2
from PIL import Image
from random import randint
import xml.etree.cElementTree as ET

przed = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','1.jpg','2.jpg','3.jpg','4.jpg','5.jpg']
po = ['1_e.jpg','2_e.jpg','3_e.jpg','4_e.jpg','5_e.jpg','1_n.jpg','2_n.jpg','3_n.jpg','4_n.jpg','5_n.jpg','1_m.jpg','2_m.jpg','3_m.jpg','4_m.jpg','5_m.jpg','1_a.jpg','2_a.jpg','3_a.jpg','4_a.jpg','5_a.jpg']

# ///////////////////////////////////////////////////////////// OBRAZ /////////////////////////////////////////////////
root = ET.Element("BC")
doc = ET.SubElement(root, "numer_indeksu").text = "142874"

for i in range(0,15):
    if(i ==0):
        oczy = ET.SubElement(root, "seria", nazwa="oczy")
    if(i ==5):
        oczy = ET.SubElement(root, "seria", nazwa="nos")
    if(i ==10):
        oczy = ET.SubElement(root, "seria", nazwa="usta")
    if(i ==15):
        oczy = ET.SubElement(root, "seria", nazwa="twarz")
    zdjecie = ET.SubElement(oczy, "zdjecie", nazwa=przed[i])
    ET.SubElement(zdjecie, "procent").text = "1%"


    im = Image.open(przed[i]) #Can be many different formats.
    pix = im.load()
    [wymiar_x , wymiar_y] = im.size
    wymiar_xy = wymiar_x * wymiar_y
    print wymiar_xy

    ET.SubElement(zdjecie, "wysokosc").text = str(wymiar_y)
    ET.SubElement(zdjecie, "szerokosc").text = str(wymiar_x)
    pixels = ET.SubElement(zdjecie, "Pixels")

    im2 = Image.open(po[i])
    pix2 = im2.load()
    zmiany = 0
    for i in range(0,wymiar_x):
        for j in range(0,wymiar_y):
            [a,b,c]=pix[i,j]
            [a1,b1,c1]=pix2[i,j]
            #if pix[i,j] <> pix2[i,j]:
            if abs(a - a1 ) >2  and abs(b - b1 )>2 and abs(b - b1 )>2:
                zmiany = zmiany +1
                ET.SubElement(pixels , "pixel", w = str(i), h=str(j) ,stary=str(pix[i,j]), nowy=str(pix2[i,j]) )

    print zmiany
tree = ET.ElementTree(root)
tree.write("filename.xml")