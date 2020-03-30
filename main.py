
#from mapping import * 
#from serial import * 
#from controls import * 
#from homography import * 
#from utils import *
from video_reader import *
import cv2
import time # remove this



if __name__ == "__main__": 
    #print("")
    #f = open("demofile2.txt", "a")
    #f.write("Now the file has more content!")
    #f.close()

    
    print("Warning: No GUI")
    reader = Reader(0, True)

    _frames = 0 
    _last_update_time = time.time()

    while True:
        img = reader.get_frame()
        
        # cv2.imshow("img", img)
        # cv2.waitKey(1)
        _frames += 1
        if _frames > 59:
            print("frame rate: {} fps".format(_frames / (time.time() - _last_update_time)))
            _frames = 0
            _last_update_time = time.time()

#    reader = Reader(0, False)
#    while True:
#        img = reader.get_frame()
#        cv2.imshow("img", img)
#        cv2.waitKey(1)
#        print("hello")
        
    #start() 

# this non-python main will be called by the wrapper gui 
#def start():
    #print("Starting maizebot...")
    #while()
