add_library('serial') 

from maze import *
from balance import *

from main import *

# map will be drawn from top right to 
maze = Maze()
balance = None

def setup():
    global maze, balance
    
    # dimension code 
    size(900, 500) # draw a 700 by 500 window
    maze.maze_width = width - 200 # maze height is determined by aspect ratio
    
    textSize(10)
    fill(0)
    text("Balance", maze.maze_width + 10, 10)
    balance = Balance(maze.maze_width + 10, 10, 50, 50, 10, 10)
    balance.draw_balance(6, 5)
    
    # setup connection to our python code 
    start() # this should start the other code
    
    
    # setup handlers
    
    
    
    # REMOVE LATER
    maze.make_fake_map()
    
def draw():
    global maze
    # check for new serial input 
    # call appropriate handlers 
    
    maze.draw_map()
    
def keyPressed(): 
    if key == 't': # to show trace
        global maze
        maze.show_trace = not maze.show_trace
        
def serialEvent(event):
    print(event.readString()) 

        
        
