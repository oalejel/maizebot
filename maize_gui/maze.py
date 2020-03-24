
class Maze: 
    
    def __init__(self):
        self.show_trace = True 
        self.maze_width = 0
        self.maze_map = list()
        self.ball_x = 0 
        self.ball_y = 0
        self.show_trace = False
    
    def draw_map(self): 
        scale_factor = min(self.maze_width / float(len(maze_map[0])), height / float(len(maze_map)))
        x = 0 
        y = 0
        noStroke()
        for r_index, row in enumerate(maze_map): 
            x = 0
            for c_index, entry in enumerate(row):
                if entry == 0: # if floor, draw white at this pixel
                    fill(255)
                elif entry == 1: # wall 
                    fill(255, 0, 0)
                else: # hole, fill with gray 
                    fill(0)
                x += scale_factor
                rect(x, y, scale_factor, scale_factor)
            y += scale_factor 
        
    def draw_controls(self): 
        global maze_width 
        fill(32, 100, 40)
    
    def update_map(self):
        pass
        
    def update_ball(self): 
        pass 
    
    def update_controls((self)): 
        pass        
    
    
    # fake map generation
    def make_fake_map(self): 
        example_width = 400
        global maze_map
        maze_map = list()
        for y in range(0, 300):
            maze_map.append([0] * example_width) # add a new row 
            for x in range(0, example_width):
                if y < 10 or y > 290 or x < 10 or x > 390:
                    maze_map[y][x] = 1
                else: 
                    maze_map[y][x] = 0
        
    
