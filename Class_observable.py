import numpy as np
import math

class observable:
    def __init__(self,name,block, LineID,position): #Position 1 for 1 entry, position 2 for 2 entries
        self.name = name
        self.value = np.array([-1e15])
        self.block = block
        self.lineID = LineID
        self.position = int(position)
        
    def set_val(self, value):
        self.value[0] = value
        
    
    def reset_val(self):
        self.value[0] = -1e15
        
        

        
        

