import numpy as np

class Procedural_object:
    def __init__(self, type):
        self.type = type
        self.position = np.array([0,0,0])
        self.scope = np.array([0,0,0])
    
    def set_type(self, type):
        self.type = type
    
    def set_position(self, position):
        self.position = position
    
    def set_scope(self, scope):
        self.scope = scope