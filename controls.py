


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

