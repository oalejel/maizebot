class Balance:
    
    
    def __init__(self, x, y, w, h, max_horizontal, max_vertical):
        self.x = x 
        self.y = y 
        self.h = h 
        self.w = w
        self.max_horizontal = max_horizontal # the maximum value along horizontal axis 
        self.max_vertical = max_vertical # the maximum value along the horizontal axis 
    
    
    def draw_balance(self, h_offset, v_offset): 
        fill(0)
        rect(self.x, self.y, self.w, self.h)
        half_x = self.x + (0.5 * self.w)
        half_y = self.y + (0.5 * self.h)
        strokeWeight(1)
        stroke(255)
        line(half_x, self.y, half_x, self.y + self.h)
        line(self.x, half_y, self.x + self.w, half_y)
        print(float(h_offset) / self.max_horizontal)
        _x = (h_offset / self.max_horizontal) * (0.5 * self.w)
        _y = (v_offset / self.max_vertical) * (0.5 * self.h)
        fill(255, 255, 0)
        circle(_x + half_x, _y + half_y, 6)
    
        
    
        
    
