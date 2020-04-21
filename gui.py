#from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import *
import time
import numpy as np
from PIL import Image, ImageTk

# Able to visualize map, updated whenever updat emap is called
# Can show and hide trace with key command 

# public interface variables:
	# show_trace, 
# public interface methods:
	# 

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
		self.maze = list() # 2d map of maze
		self.maze_w = 300
#		self.maze_h = 200
		self.canvas_h = 300
		self.canvas_w = 500
		self.maze_array = maze_array # save np.ndarray representing maze
		
		self.initUI()
		
#		self.make_fake_map()
		self.colorize_map() # converts to red white and black
		self.draw_map()
		print("done drawing map")
		# warning: may need to put this on a separate thread
		self.master.mainloop()

	def initUI(self):
#		self.root.geometry("400x250")
		self.master.title("MaizeBot GUI")
#		self.masterpack(side = TOP, pady = 5)

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
		
	def setMap(self, map_data):
		pass 
	
	def updateBall(self, x, y): 
		self.trace.append(x, y, time.time())
#		self.canvas.create_
		
	# convert map of 0,1,2 to colors 
	def colorize_map(self): 
		color_arr = np.ndarray(shape=(self.maze_array.shape[0], self.maze_array.shape[1], 3))
		color_arr[:,:,0] = (self.maze_array[:, :] == 1) * 255 # red if 1
		color_arr[:,:,0] = (self.maze_array[:, :] == 2) * 125 # gray if 2
		color_arr[:,:,1] = (self.maze_array[:, :] == 2) * 125 # gray if 2
		color_arr[:,:,2] = (self.maze_array[:, :] == 2) * 125 # gray if 2
		
		# save our maze array to color 
		self.maze_array = color_arr
#		print(self.maze_array.shape)
#		quit()
#		self.maze_array[x==1] = 
#		0 empty 1 wall, 2 hole
		
	# called when we want to refresh the map????
	def draw_map(self):
		# Image.
		print(self.maze_array.dtype)
		maze_img = ImageTk.PhotoImage(image=Image.fromarray(self.maze_array.astype(np.uint8)))
		self.maze_img = maze_img # avoid garbage collection
		self.canvas.create_image(0, 0, image=maze_img, anchor=NW)
#		print("here")
#		self.maze_scale = min(self.maze_w / float(len(self.maze[0])), self.canvas_h / float(len(self.maze)))
#		x = 0 
#		y = 0
#		for r_index, row in enumerate(self.maze): 
#			x = 0
#			for c_index, entry in enumerate(row):
#				if entry == 0: # if floor, draw white at this pixel
#					self.canvas.create_rectangle(x, y, self.maze_scale, self.maze_scale, fill="white")
#				elif entry == 1: # wall 
#					self.canvas.create_rectangle(x, y, self.maze_scale, self.maze_scale, fill="red")
#				else: # hole, fill with gray 
#					self.canvas.create_rectangle(x, y, self.maze_scale, self.maze_scale, fill="gray")
#				x += self.maze_scale
#				
#			y += self.maze_scale 
#		print("here2")

		
		

	# MOCK DATA 
	
#	def make_fake_map(self): 
#		array = np.zeros((100,50))
#		array[0:40] = 125
#		maze_img = ImageTk.PhotoImage(image=Image.fromarray(array))
#		self.maze_img = maze_img # avoid garbage collection
#		self.canvas.create_image(0, 0, image=maze_img, anchor=NW)
		
#		self.maze = list()
#		for y in range(0, self.canvas_h):
#			self.maze.append([0] * self.maze_w) # add a new row 
#			for x in range(0, self.maze_w):
#				if y < 10 or y > 290 or x < 10 or x > 390:
#					self.maze[y][x] = 1
#				else: 
#					self.maze[y][x] = 0
			

# test map
# array = np.zeros((100,50))
# array[0:40] = 125

# # comment out
# ex = MazeGUI(array)
