


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
        
        # tune these parameters. not necessary for motors to have same ks
        self.pid_x = StepperPID(kP = 0.1, kI = 0.0, kD = 0.0)
        self.pid_y = StepperPID(kP = 0.1, kI = 0.0, kD = 0.0)

        # split up the path into line segments 
        self.path_steps = [] # list of coordinates, forming straight lines in between each other
        seg_start_idx = 0
        
        for (idx, coord) in enumerate(path): 
            # if coord strays off of the line segment from 'seg_start_idx' to 'idx',
            #    then add (seg_start_idx, idx) to the segments list, then set seg_start_idx = idx (+ 1?)
            
            if (not is_valid_line(seg_start_idx, idx)):
                self.path_steps.add(path[idx - 1])
                seg_start_idx = idx

        self.step_idx = 1 # index of aggregated path step we are traveling to

    
    def update_ball(self, x, y): 
        # start_coord = self.path_steps[self.step_idx - 1] # ex: (0, 4) means checking cell 0 and cell 4
        end_coord = self.path_steps[self.step_idx]
        x_error = end_coord[0] - x 
        y_error = end_coord[1] - y 
        
        # use position and Derror threshold to determine whether we have reached end_coord
        if x_error < 7 and y_error < 7 and abs(x_error - self.pid_x.last_error) < 3 and abs(y_error - self.pid_y.last_error):
            # move on to next target coordinate
            self.step_idx += 1
            self.pid_x.reset() 
            self.pid_y.reset() 
        else:
            # prepare angle command for motors 
            # warning: consider making the pid to motor angle relationship non-linear (i.e. with a log or something)
            rotx = self.pid_x.update(x_error)
            roty = -1 * self.pid_y.update(y_error)
            
            # PSEUDOCODE for telling serial to move motors 
            serial.motor_update(rotx, roty)

        # warning: may need to check for getting stuck / going off-path 
        

            
