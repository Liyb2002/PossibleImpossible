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

        len_x = round(random.uniform(scope_x[0], scope_x[1]),4)
        len_y = round(random.uniform(scope_y[0], scope_y[1]),4)
        len_z = round(random.uniform(scope_z[0], scope_z[1]),4)
        self.length = np.array([len_x, len_y, len_z])

    def set_position(self, prev_obj, rule):
        prev_pos = prev_obj.position
        prev_x = prev_obj.length[0]
        prev_y = prev_obj.length[1]
        prev_z = prev_obj.length[2]

        if(rule == '-x'):
            self.position = prev_pos - np.array([prev_x, 0, 0]) - np.array([self.length[0],0,0])

        if(rule == '+x'):
            self.position = prev_pos + np.array([prev_x, 0, 0]) + np.array([self.length[0],0,0])
        
        if(rule == '-y'):
            self.position = prev_pos - np.array([0, prev_y, 0]) - np.array([0,self.length[1],0])
        
        if(rule == '+y'):
            self.position = prev_pos + np.array([0, prev_y, 0]) + np.array([0,self.length[1],0])
       
        if(rule == '-z'):
            self.position = prev_pos - np.array([0, 0, prev_z]) - np.array([0,0,self.length[2]])

        if(rule == '+z'):
            self.position = prev_pos + np.array([0, 0, prev_z]) + np.array([0,0,self.length[2]])

        self.arriving_rule = rule
        
    def arbitrary_set_position(self, position):
        self.position = position

    def collision_check(self, objB):
        for i in range(3):
            A_x = [self.position[i] - self.length[i], self.position[i] + self.length[i]]
            B_x = [objB.position[i] - objB.length[i], objB.position[i] + objB.length[i]]
            overlap_x = getOverlap(A_x, B_x)
            if overlap_x> 0.05:
                return True
        return False


def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))
