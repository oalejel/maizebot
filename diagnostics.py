import time 

# used for things like tracking the framerate 

class Diagnostics:
    def __init__(self):
        self.frame_count = 0 
        self.last_update_time = time.time()
        self.disabled = False

    # updates framerate measurement by indicating that a new frame was read in
    def newFrame(self): 
        self.frame_count += 1
        if self.frame_count > 59:
            print("frame rate: {} fps".format(self.frame_count / (time.time() - self.last_update_time)))
            self.frame_count = 0
            self.last_update_time = time.time()


