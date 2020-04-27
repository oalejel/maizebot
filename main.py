from maze import Maze 
from controls import Controller
from planning import Planner
from gui import MazeGUI
from video_reader import *
from diagnostics import *
import cv2
import threading
import time

GUI_ENABLED = True

def main(): 
    # prepare higher level objects    
    reader = Reader(2, True)
    diagnostics = Diagnostics()
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (640,480))

    # Read first frame to generate map
    for i in range(30):
        img = reader.get_frame()
    img = reader.get_frame()
    maze = Maze(img)
    gui = MazeGUI(maze.map) if GUI_ENABLED else None
    
    # code encapsulating all non-gui processing, placed on another thread
    # all variables declared above will be visible to the thread calling run_maizebot
    def run_maizebot(img):
        # prepare path planner to construct a path, construct the controller, and start localization->control loop
        maze.detect_ball(img, 1)
        #planner = Planner(maze)
        #planner.plan_path()
        #planner.aggregate_path()
        path = [(25,30),(15,238),(55, 238),(272,143),(272, 323), (10, 300), (105, 380), (15, 480),(165, 480),(245, 360), (335, 440), (450, 285),
                (315, 323),(315, 180),(560,120), (430,20), (680, 20), (680, 115), (600, 150),(680, 250), (600,325), (680, 480), (580, 480),(500, 370), (500, 480), (210, 480)]
        controller = Controller(path)
        gui.set_path(path)

        while True:
            img = reader.get_frame()
            out.write(img)
            current_location = maze.detect_ball(img, time.time())
            gui.update_ball(current_location[1], current_location[0])
            controller.update_ball(current_location)
            gui.set_subpath_idx(controller.path_idx)
            # tell diagnostics that we have received a new camera frame. comment if no diagnostics desired
            diagnostics.newFrame()

    if GUI_ENABLED:
        # create thread for maizebot mapping, controls, etc to run separate from GUI
        thread = threading.Thread(target=run_maizebot, args=[img])
        thread.start()
        gui.run() # blocking run on main thread
        thread.join() # wait for run_maizebot to complete execution (so that killing gui doesnt kill maizebot)
        # code after the line above will not execute, as gui begins a graphics runloop on main
    else: 
        run_maizebot(img)
    

    
if __name__ == "__main__": 
    main()