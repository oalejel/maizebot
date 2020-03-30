add_library('serial')

from maze import *
from balance import *
import socket

# map will be drawn from top right to 
maze = Maze()
balance = None

def setup():
    global maze, balance
    
    HOST = 'me'                 # Symbolic name meaning all available interfaces
    PORT = 6969               # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    # s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        print("waiting on data")
        data = conn.recv(1024)
        print("got data")
        if not data: break
        print(data) # Paging Python!
        # do whatever you need to do with the data
    conn.close()
    
    # dimension code 
    size(900, 500) # draw a 700 by 500 window
    maze.maze_width = width - 200 # maze height is determined by aspect ratio
    
    textSize(10)
    fill(0)
    text("Balance", maze.maze_width + 10, 10)
    balance = Balance(maze.maze_width + 10, 10, 50, 50, 10, 10)
    balance.draw_balance(6, 5)
    
    # setup connection to our python code 
    # exec(open('../main.py').read())

    # start() # this should start the other code
    
    
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

# import processing.net.*; 

# Client myClient; 
# int dataIn; 
 
# void setup() { 
#   size(200, 200); 
#   // Connect to the local machine at port 5204.
#   // This example will not run if you haven't
#   // previously started a server on this port.
#   myClient = new Client(this, "127.0.0.1", 5204); 
# } 
 
# void draw() { 
#   if (myClient.available() > 0) { 
#     dataIn = myClient.read(); 
#   } 
#   background(dataIn); 
# } 



        
        
