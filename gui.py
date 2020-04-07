#from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import *
import time

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

	def __init__(self):
		super().__init__()
		
		self.show_trace = False
		self.trace = list() # pairs of (x, y, time)
		self.maze = list() # 2d map of maze
		self.maze_w = 300
		self.maze_h = 200
		
		
		self.initUI()
		# warning: may need to put this on a separate thread
		self.master.mainloop()

	def initUI(self):
#		self.root.geometry("400x250")
#		self.master.title("Lines")
#		self.masterpack(side = TOP, pady = 5)

		canvas = Canvas(self.master, width=600, height=400)#, bg="blue")
		canvas.create_rectangle(0, 0, 100, 100, fill="red")
		canvas.pack()
		canvas.create_line(15, 25, 200, 25)
		canvas.create_line(300, 35, 300, 200, dash=(4, 2))
		canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
		
		canvas.bind("<Key>", self.key)
#		canvas.bind("<Button-1>", self.) # for mouse clicks
		canvas.pack(fill=BOTH, expand=2)
		self.canvas = canvas 
		
	def setMap(map_data):
		pass 
	
	def updateBall(x, y): 
		self.trace.append(x, y, time.time())
		
		
		
	# MOCK DATA 
	
	def make_fake_map(self): 
		self.maze = list()
		for y in range(0, 300):
			self.maze.append([0] * self.maze_h) # add a new row 
			for x in range(0, self.maze_w):
				if y < 10 or y > 290 or x < 10 or x > 390:
					self.maze[y][x] = 1
				else: 
					self.maze[y][x] = 0
			

	
	
	
# comment out
ex = MazeGUI()
