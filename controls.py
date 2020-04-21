from time import time, sleep
import struct
import serial


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
        self.prev_target_vx = 0.0
        self.prev_target_vy = 0.0
        
        #params
        self.pos_tolerance = 40 #in pixels
        self.v_tolerance = 5 #in px/sec
        self.target_v = 3 #in px/sec


        # tune these parameters. not necessary for motors to have same ks
        self.pid_x = StepperPID(kP = 1, kI = 0.0, kD = 0.0)
        self.pid_y = StepperPID(kP = 0.1, kI = 0.0, kD = 0.0)
        self.ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
        sleep(2)
        

    
    def update_ball(self, update):
        # start_coord = self.path_steps[self.step_idx - 1] # ex: (0, 4) means checking cell 0 and cell 4

        curr_goal = self.path[self.path_idx]
        delta_x = curr_goal[0] - update[0]
        delta_y = curr_goal[1] - update[1]
        print("dx={}, dy={}, target pos: ({},{})".format(delta_x, delta_y, curr_goal[0], curr_goal[1]))

        if abs(update[2]) + abs(update[3]) < 2 * self.v_tolerance and abs(delta_x) + abs(delta_y) < 2 * self.pos_tolerance: #stopped at goal and ready to move on to next one
            self.path_idx += 1
            print("Moving to subpath at index {}".format(self.path_idx))
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
        rotx = self.pid_x.update(target_vx - update[2])
        roty = self.pid_y.update(target_vy - update[3])

        dirx = 0
        diry = 1    
        if rotx > 0:
            dirx = 1
        if roty > 0:
            diry = 0
        rotx = abs(rotx)
        roty = abs(roty)
        if(rotx > 5):
            rotx = 5
        if roty > 5:
            roty = 5

        print(diry, int(abs(roty)), dirx, int(abs(rotx)))
        
        self.ser.write(struct.pack('>BBBB',dirx, int(abs(rotx)), diry, int(abs(roty))))
        

            
