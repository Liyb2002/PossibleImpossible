import numpy as np
import random

class Procedural_object:
    def __init__(self, type, position, scope):
        self.type = type
        self.position = position
        self.scope = scope

        self.set_scope()
    
    def set_type(self, type):
        self.type = type
    
    def set_scope(self):
        scope_x = self.scope[0]
        scope_y = self.scope[1]
        scope_z = self.scope[2]

        self.len_x = round(random.uniform(scope_x[0], scope_x[1]),2)
        self.len_y = round(random.uniform(scope_y[0], scope_y[1]),2)
        self.len_z = round(random.uniform(scope_z[0], scope_z[1]),2)

    def arbitrary_set(self, position):
        self.position = position
        
    def set_position(self, prev_obj, rule):
        prev_pos = prev_obj.position
        prev_x = prev_obj.len_x
        prev_y = prev_obj.len_y
        prev_z = prev_obj.len_z

        if(rule == '-x'):
            self.position = prev_pos - np.array([prev_x, 0, 0]) - np.array([self.len_x,0,0])

        if(rule == '+x'):
            self.position = prev_pos + np.array([prev_x, 0, 0]) + np.array([self.len_x,0,0])
        
        if(rule == '-y'):
            self.position = prev_pos - np.array([0, prev_y, 0]) - np.array([0,self.len_y,0])
        
        if(rule == '+y'):
            self.position = prev_pos + np.array([0, prev_y, 0]) + np.array([0,self.len_y,0])
       
        if(rule == '-z'):
            self.position = prev_pos - np.array([0, 0, prev_z]) - np.array([0,0,self.len_z])

        if(rule == '+z'):
            self.position = prev_pos + np.array([0, 0, prev_z]) + np.array([0,0,self.len_z])
