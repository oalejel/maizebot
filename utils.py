
# using python data classes 
@dataclass
class pose:
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0 
    vy: float = 0.0

@dataclass
class cell:
    
@dataclass
class map:
    






# old defintion of pose, not using @dataclass 
# class pose:
#     def __init__(self, x=0, y=0, vx=0, vy=0): 
#         self.x = x
#         self.y = y 
#         self.vx = vx 
#         self.vy = vy 