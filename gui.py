#from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import *
import time
import numpy as np
from PIL import Image, ImageTk
from numpy import asarray
import math
import threading

# Able to visualize map, updated whenever updat emap is called
# Can show and hide trace with key command 

# public interface variables:
	# show_trace, 
# public interface methods:

class MazeGUI(Frame): 
	
	def key(self, event):
		if (event.char == 't'):
			self.show_trace = not self.show_trace
			print("toggle show_trace")

	def callback(self, event):
		pass
#		self.canvas.focus_set()
#		print("clicked at", event.x, event.y)

	def __init__(self, maze_array):
		super().__init__()
		
		self.show_trace = False
		self.trace = list() # pairs of (x, y, time)
		
		self.maze_array = maze_array # save np.ndarray representing maze
		
		# compute dimensions of canvas to fit maze, potentially scaling
		MINIMUM_HEIGHT = 300
		PANEL_WIDTH = 200
		PANEL_PADDING = 20
		self.scale_factor = math.ceil(MINIMUM_HEIGHT / maze_array.shape[0])
		self.canvas_h = self.scale_factor * self.maze_array.shape[0]
		self.canvas_w = self.scale_factor * self.maze_array.shape[1] + PANEL_WIDTH
		
		self.initUI()
		
		self.generate_map_image() # converts to red white and black
		self.redraw_map_image()
		
		# warning: may need to put this on a separate thread
		self.master.mainloop()

	def initUI(self):
#		self.root.geometry("400x250")
		self.master.title("MaizeBot GUI")

		canvas = Canvas(self.master, width=self.canvas_w, height=self.canvas_h)#, bg="blue")
#		canvas.create_rectangle(0, 0, 100, 100, fill="red")
		canvas.pack()
#		canvas.create_line(15, 25, 200, 25)
#		canvas.create_line(300, 35, 300, 200, dash=(4, 2))
#		canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
		
		canvas.bind("<Key>", self.key)
#		canvas.bind("<Button-1>", self.) # for mouse clicks
		canvas.pack(fill=BOTH, expand=2)
		self.canvas = canvas 
		
	def setMap(map_data):
		pass 
	
	def updateBall(x, y): 
		self.trace.append(x, y, time.time())
		self.circle = self.canvas.create_circle(20, x, y, fill="#BBB", outline="")
		print(self.circle)
#		self.canvas.create_
		
	# convert map of 0,1,2 to colors 
	def generate_map_image(self): 
		# 0 empty 1 wall, 2 hole
		color_arr = np.ndarray(shape=(self.maze_array.shape[0], self.maze_array.shape[1], 3))
		color_arr[self.maze_array[:, :] == 1,0] = 255 # red if 1
		color_arr[self.maze_array[:, :] == 2,0:3] = 125 # gray if 2
				
		# save our maze array to color 
		self.maze_array = color_arr
		
		img = Image.fromarray(np.uint8(self.maze_array))
		maze_img = ImageTk.PhotoImage(image=img.resize((self.scale_factor * self.maze_array.shape[1], self.scale_factor * self.maze_array.shape[0])))
		self.maze_img = maze_img # avoid garbage collection

			
	def redraw_map_image(self): 
		self.canvas.create_image(0, 0, image=self.maze_img, anchor=NW)

	

#def main(): 
#	# test map
#	array = np.ones((500,700))
#	array[20:480, 20:680] = 0
#		
#	# comment out
#	ex = MazeGUI(array)
#
#main()





"""
Multithreading testing:
	


class Test: 
	def __init__(self): 
		self.foo = 50
		
	def print_foo(self):
		print(self.foo)
		self.foo = self.foo + 1

def run_maizebot(): 
	x = 0
	while x != 1001: 
		x = x + 2 
		print(x)

	

def main(): 
	t = Test()
	# test map
	array = np.ones((500,700))
	array[20:480, 20:680] = 0
	
	t.print_foo()
	print("first")
	def do_stuff(): 
		time.sleep(4)
		t.print_foo()
		print("second")
		print("--- IM PRINTING {} ---".format(array.shape))
	
	thread = threading.Thread(target=do_stuff, args=())
#	thread = threading.Thread(target=run_maizebot, args=())
	thread.start()   
	
	t.print_foo()
	print("third")
	
	# comment out
	ex = MazeGUI(array, t)

main()



"""
