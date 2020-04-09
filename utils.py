from dataclasses import dataclass
from enum import IntEnum
import constants
import numpy as np
# using python data classes 
@dataclass
class Pose:
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0 
    vy: float = 0.0

class Cell(IntEnum):
    FREE = 0
    WALL = 1
    HOLE = 2
    







# old defintion of pose, not using @dataclass 
# class pose:
#     def __init__(self, x=0, y=0, vx=0, vy=0): 
#         self.x = x
#         self.y = y 
#         self.vx = vx 
#         self.vy = vy 