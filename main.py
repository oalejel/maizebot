
from mapping import * 
from serial import * 
from controls import * 
from homography import * 
#from utils import *
from video_reader import *
import cv2

if __name__== "__main__":
    print("Warning: No GUI")
    reader = Reader(0, False)
    while True:
        img = reader.get_frame()
        cv2.imshow("img", img)
        cv2.waitKey(1)
    #start() 

# this non-python main will be called by the wrapper gui 
#def start():
    #print("Starting maizebot...")
    #while()
