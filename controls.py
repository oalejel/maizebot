<<<<<<< HEAD
from time import time #using system time for now, we might want to change that


# PID controller for a single stepper motor, issuing relative angle changes
# and basing error off of whatever localization parameter you like (in this case, we use displacement)
class StepperPID: 

    def __init__(self, kP = 0.1, kI = 0.0, kD = 0.0):
        self.angle = 0 # command of no stepper motor motion
        self.integral = 0 
        self.last_error = 0

        # tune these parameters in the constructor
        self.kP = kP
        self.kI = kI
        self.kD = kD 
        
    # pass in new errors for updated angles
    def update(self, error):
        self.integral += error 
        self.angle = (self.kP * error) + (self.kI * self.integral) + (self.kD * (error - self.last_error))
        self.last_error = error

        return self.angle

    # reset integral and other parameters when moving to the next goal?
    def reset(self): 
        # warning: not sure if all of these should be set back to zero 
        self.integral = 0 
        self.last_error = 0 
        self.angle = 0

class Controller: 

    def __init__(self, path): 
        self.path = path
        self.path_idx = 0
        self.x = 0.0
        self.y = 0.0
        self.prev_target_vx = 0.0
        self.prev_target_vy = 0.0
        self.time = time()
        
        #params
        self.pos_tolerance = 5 #in pixels
        self.v_tolerance = .2 #in px/sec
        self.target_v = 1 #in px/sec


        # tune these parameters. not necessary for motors to have same ks
        self.pid_x = StepperPID(kP = 0.1, kI = 0.0, kD = 0.0)
        self.pid_y = StepperPID(kP = 0.1, kI = 0.0, kD = 0.0)

    
    def update_ball(self, x, y):
        # start_coord = self.path_steps[self.step_idx - 1] # ex: (0, 4) means checking cell 0 and cell 4
        curr_time = time()
        delta_t = curr_time - self.time
        self.time = curr_time
        vx = (x - self.x)/delta_t
        vy = (y - self.y)/delta_t
        self.x = x
        self.y = y

        curr_goal = self.path[self.path_idx]
        delta_x = curr_goal[0] - x
        delta_y = curr_goal[1] - y

        if abs(vx) + abs(vy) < 2 * self.v_tolerance and abs(delta_x) + abs(delta_y) < 2 * self.pos_tolerance: #stopped at goal and ready to move on to next one
            self.path_idx += 1
            self.pid_x.reset()
            self.pid_y.reset()
            return
        
        if abs(delta_x) < self.pos_tolerance:
            target_vx = 0
        elif delta_x > 0:
            target_vx = self.target_v
        else:
            target_vx = -self.target_v

        if abs(delta_y) < self.pos_tolerance:
            target_vy = 0
        elif delta_y > 0:
            target_vy = self.target_v
        else:
            target_vy = -self.target_v

        #if target velocities changed, reset pid state
        if target_vx != self.prev_target_vx:
            self.prev_target_vx = target_vx
            self.pid_x.reset()

        if target_vy != self.prev_target_vy:
            self.prev_target_vy = target_vy
            self.pid_y.reset()

        #might need to adjust signs here
        rotx = self.pid_x.update(target_vx - vx)
        roty = self.pid_y.update(target_vy - vy)
            
        # PSEUDOCODE for telling serial to move motors 
        serial.motor_update(rotx, roty)
        

            
=======
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
>>>>>>> planning
