from tkinter import *
import time
import numpy as np
from PIL import Image, ImageTk
from numpy import asarray
import math
import threading

class MazeGUI(Frame): 
	
	def key(self, event):
		if (event.char == 't'):
			print("toggle show_trace")

	def callback(self, event):
		pass

	def __init__(self, maze_array):
		super().__init__()
		
		
		self.maze_array = maze_array # save np.ndarray representing maze
		
		# compute dimensions of canvas to fit maze, potentially scaling
		MINIMUM_HEIGHT = 300
		PANEL_WIDTH = 200
		PANEL_PADDING = 20
		self.scale_factor = math.ceil(MINIMUM_HEIGHT / maze_array.shape[0])
		self.canvas_h = self.scale_factor * self.maze_array.shape[0]
		self.canvas_w = self.scale_factor * self.maze_array.shape[1]
		self.labels = {}
		
		self.initUI() # prepare canvas
		
		# bind keys for toggles
		self.canvas.bind("<Key>", self.key)

		# add new helpers to canvas object 
		def _create_circle(self, x, y, r, **kwargs):
				return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
		Canvas.create_circle = _create_circle

	def run(self):
		self.master.mainloop()

	def initUI(self):
		self.master.title("MaizeBot GUI")

		canvas = Canvas(self.master, width=self.canvas_w, height=self.canvas_h)#, bg="blue")
		canvas.pack(side="left")
		self.canvas = canvas 
		
		self.pinball = None
		self.subpath_idx = 0
		self.subpath_line = None
		
		# prepare first version of UI
		self.generate_map_image() # converts to red white and black
		self.redraw_map_image()

			
	def update_ball(self, x, y): 
		if self.pinball is None:
			self.pinball = self.canvas.create_circle(x, y, 20, fill="#00F", outline="")
		else: 
			self.canvas.move(self.pinball, x - self.ball_pos[0], y - self.ball_pos[1])
		self.ball_pos = (x, y)


	def set_subpath_idx(self, idx): 
		if self.path is None:
			pass

		if self.subpath_idx != idx:
			if self.subpath_line != None: 
				self.canvas.delete(self.subpath_line)
			(x0, y0) = (self.path[idx])
			(x1, y1) = (self.path[idx-1])
			self.subpath_line = self.canvas.create_line(x0, y0, x1, y1, fill="#0F0")
			self.subpath_idx = idx
		
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

	def set_path(self, path): # draw points along the path 
		self.path = path
		for x, y in path:
			self.canvas.create_circle(x, y, 2, fill="#00FF00", outline="")
			
	def redraw_map_image(self): 
		self.canvas.create_image(0, 0, image=self.maze_img, anchor=NW)

	def update_label(self, name, text):
		if name not in self.labels: 
			w = Label(self.master, text=text, width=20)
			w.pack(anchor=NE, side="right", padx=5) 

			self.labels[name] = w
		else:
			self.labels[name].configure(text=text) 
		print(len(text))