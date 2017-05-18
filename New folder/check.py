__author__ = 'Jasiu'
import ctypes
from ctypes import *
from PIL import Image

windll.kernel32.GetModuleHandleW(0)

im = Image.open('1.jpg') #Can be many different formats.
pix = im.load()

lib = ctypes.WinDLL('C:\Users\Jasiu\Downloads\dlls\dlls\FaceRecognitionDll.dll')

func = lib['CheckPhoto']
func.restype = ctypes.c_image
value = func(ctypes.c_image())