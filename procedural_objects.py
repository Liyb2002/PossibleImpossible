import numpy as np
import random

class Procedural_object:
    def __init__(self, type, position, scope, gen_hash, next_rotation):
        self.type = type
        self.position = position
        self.scope = scope
        self.set_scope()
        self.hash = gen_hash
        self.connected = []
        self.rotation = np.array([random.choice(next_rotation[0]), random.choice(next_rotation[1]), random.choice(next_rotation[2])])

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

        if(rule == '-x2'):
            self.position = prev_pos - np.array([prev_x, -prev_y, 0]) - np.array([self.length[0],0 ,0])
            self.arriving_rule = '-x'
            
        self.arriving_rule = rule

    def arbitrary_set_position(self, position):
        self.position = position

    def collision_check(self, objB):
        A_x = [self.position[0] - self.length[0], self.position[0] + self.length[0]]
        B_x = [objB.position[0] - objB.length[0], objB.position[0] + objB.length[0]]
        overlap_x = getOverlap(A_x, B_x)

        A_y = [self.position[1] - self.length[1], self.position[1] + self.length[1]]
        B_y = [objB.position[1] - objB.length[1], objB.position[1] + objB.length[1]]
        overlap_y = getOverlap(A_y, B_y)

        A_z = [self.position[2] - self.length[2], self.position[2] + self.length[2]]
        B_z = [objB.position[2] - objB.length[2], objB.position[2] + objB.length[2]]
        overlap_z = getOverlap(A_z, B_z)

        if overlap_x>0.0 and overlap_y>0.0 and overlap_z>0.0:
            # print("cur obj", self.position, self.length)
            # print("objB", objB.position, objB.length)
            return True

        return False
    
    def add_connected(self, direction):
        for dir in self.connected:
            if dir == direction:
                return 
        self.connected.append(direction)

    def arbitrary_set_length(self, length):
        len_x = length[0]
        len_y = length[1]
        len_z = length[2]
        self.length = np.array([len_x, len_y, len_z])


def getOverlap3D(objectA_position, objectA_size, objectB_position, objectB_size):
    A_x = [objectA_position[0] - objectA_size[0], objectA_position[0] + objectA_size[0]]
    B_x = [objectB_position[0] - objectB_size[0], objectB_position[0] + objectB_size[0]]
    overlap_x = getOverlap(A_x, B_x)

    A_y = [objectA_position[1] - objectA_size[1], objectA_position[1] + objectA_size[1]]
    B_y = [objectB_position[1] - objectB_size[1], objectB_position[1] + objectB_size[1]]
    overlap_y = getOverlap(A_y, B_y)

    A_z = [objectA_position[2] - objectA_size[2], objectA_position[2] + objectA_size[2]]
    B_z = [objectB_position[2] - objectB_size[2], objectB_position[2] + objectB_size[2]]
    overlap_z = getOverlap(A_z, B_z)

    return overlap_x * overlap_y * overlap_z

def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))
