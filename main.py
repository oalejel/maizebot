
#from mapping import * 
#from serial import * 
#from controls import * 
#from homography import * 
#from utils import *
from video_reader import *
from diagnostics import *
import cv2
import threading

GUI_ENABLED = True # try disabling to compare performance. may need to fix some thread task queueing

def main(): 
    # prepare higher level objects    
    reader = Reader(0, True)
    diagnostics = Diagnostics()

    # Read first frame to generate map
    img = reader.get_frame()
    mapping = Map(img)
    gui = MazeGUI(mapping.map) if GUI_ENABLED else None
    # code encapsulating all non-gui processing, placed on another thread
    # all variables declared above will be visible to the thread calling run_maizebot
    # warning: some shared variables may require a lock
    def run_maizebot():
        controller = Controller()

        while True:
            img = reader.get_frame()
            current_location = mapping.detect_ball()
            gui.updateBall(current_location[0], current_location[1])
            controller.update_ball(current_location[0], current_location[1])
            # cv2.imshow("img", img)
            # cv2.waitKey(1)
            # tell diagnostics that we have received a new camera frame. comment if no diagnostics desired
            diagnostics.newFrame()

    if GUI_ENABLED:
        # create thread for maizebot mapping, controls, etc to run separate from GUI
        thread = threading.Thread(target=run_maizebot, args=())
        thread.start()   
        gui.run() # blocking run on main thread
        thread.join() # wait for run_maizebot to complete execution (so that killing gui doesnt kill maizebot)
        # code after the line above will not execute, as gui begins a graphics runloop on main
    else: 
        run_maizebot()
    

    
if __name__ == "__main__": 
    main()