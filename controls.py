from gekko import GEKKO
import numpy as np

m = GEKKO() #initialize gekko object
m.time = np.linspace(0, 20, 50) #50 evenly spaced samples in the range 0-20

#parameters (put parameters which belong in the model below)

# mainipulated variable
x_theta = m.MV(value = 0, lb = -(np.pi/6), np.pi/6) #starting value of 0 (centered) bounded so the rotation is no more than 30 degrees off center 
x_theta.STATUS = 1 #allows optimizer to change this value
x_theta.DCOST = 0 #add a cost to changing this variable, increasing this has a smoothing effect
x_theta.DMAX = np.pi/12 #max change in angle between each time step

y_theta = m.MV(value = 0, lb = -(np.pi/6), np.pi/6) #starting value of 0 (centered) bounded so the rotation is no more than 30 degrees off center 
y_theta.STATUS = 1 #allows optimizer to change this value
y_theta.DCOST = 0 #add a cost to changing this variable, increasing this has a smoothing effect
y_theta.DMAX = np.pi/12 #max change in angle between each time step

#controlled variable
x_pos = m.CV(value=0) #starting value is 0
x_pos.STATUS = 1 #allow this to be added to the objective function
#figure out how to set a loss function

#model
m.Equation() #put x equation here
m.Equation() #put y equation here

m.options.IMODE = 6
m.solve(disp=False)
