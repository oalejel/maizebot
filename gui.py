#from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import *

# Able to visualize map, updated whenever updat emap is called
# Can show and hide trace with key command 

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
		
		self.initUI()

		# warning: may need to put this on a separate thread
		self.master.mainloop()

	def initUI(self):
#		self.root.geometry("400x250")
#		self.master.title("Lines")
#		self.masterpack(side = TOP, pady = 5)

		canvas = Canvas(self.master, width=600, height=400)#, bg="blue")
		canvas.pack()
		canvas.create_line(15, 25, 200, 25)
		canvas.create_line(300, 35, 300, 200, dash=(4, 2))
		canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
		
		canvas.bind("<Key>", self.key)
		canvas.bind("<Button-1>", self.callback)
		canvas.pack(fill=BOTH, expand=2)
		self.canvas = canvas 
		
	def setMap(map_data):
		pass 
	
	
		
		
	
ex = MazeGUI()
	
#
#from Tkinter import *
#
#master = Tk()
#
#w = Canvas(master, width=200, height=100)
#w.pack()
#
#w.create_line(0, 0, 200, 100)
#w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
#
#w.create_rectangle(50, 25, 150, 75, fill="blue")
#
#mainloop()
