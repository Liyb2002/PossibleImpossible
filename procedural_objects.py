import numpy as np

class Procedural_object:
    def __init__(self, type, position, scope):
        self.type = type
        self.position = position
        self.scope = scope
    
    def set_type(self, type):
        self.type = type
    
    def set_position(self, prev_obj, rule):
        prev_pos = prev_obj.position
        prev_scope = prev_obj.scope
        if(rule == '-x'):
            self.position = prev_pos - np.array([prev_scope[0], 0, 0]) - np.array([self.scope[0],0,0])

        if(rule == '+x'):
            self.position = prev_pos + np.array([prev_scope[0], 0, 0]) + np.array([self.scope[0],0,0])
        
        if(rule == '-y'):
            self.position = prev_pos - np.array([0, prev_scope[1], 0]) - np.array([0,prev_scope[1],0])
        
        if(rule == '+y'):
            self.position = prev_pos + np.array([0, prev_scope[1], 0]) + np.array([0,prev_scope[1],0])
       
        if(rule == '-z'):
            self.position = prev_pos - np.array([0, 0, prev_scope[2]]) - np.array([0,0,prev_scope[2]])

        if(rule == '+z'):
            self.position = prev_pos + np.array([0, 0, prev_scope[2]]) + np.array([0,0,prev_scope[2]])

    def set_scope(self, scope):
        self.scope = scope