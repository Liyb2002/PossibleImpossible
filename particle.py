import produce
import cycle_connect
import random
import procedural_objects
import numpy as np

class Particle:
    def __init__(self, generic_object_list):
        self.generic_object_list = generic_object_list
        self.success = True
        self.procedural_objects = []


    def run_particle(self,intersection, start_type, steps, isFront):
        cur_obj = start_obj(intersection, self.generic_object_list, start_type)
        self.procedural_objects.append(cur_obj)

        if isFront:
            self.procedural_objects += produce.execute_model(self.generic_object_list, cur_obj, steps)
            self.start_connect = self.procedural_objects[-1]
        else:
            self.procedural_objects += produce.execute_model(self.generic_object_list, cur_obj, steps)
            self.end_connect = self.procedural_objects[-1]

    def run_connect(self):
        connect_list = cycle_connect.solve_3D(self.generic_object_list, self.start_connect, self.end_connect)
        if len(connect_list) == 0:
            print("failed connect")
            self.success = False
        else:
            print("success connect")
        self.procedural_objects += connect_list
    
    def run_particle2(self, steps):
        rd1, rd2 = self.random_object()
        objStart = self.procedural_objects[rd1]
        objStart2 = self.procedural_objects[rd2]

        self.procedural_objects += produce.execute_model(self.generic_object_list, objStart, steps)
        self.start_connect = self.procedural_objects[-1]
        self.procedural_objects += produce.execute_model(self.generic_object_list, objStart2, steps)
        self.end_connect = self.procedural_objects[-1]

    def overlapping_check(self):
        for obj_A in self.procedural_objects:
            for obj_B in self.procedural_objects:
                if obj_A.hash != obj_B.hash:
                    overlapping = obj_A.collision_check(obj_B)
                    if overlapping:
                        self.success = False
            
    def find_connect_ending(self):
        for obj in self.back_list:
            if obj.type == 1:
                return obj
    
    def random_object(self):
        rd1 = 0
        rd2 = 0

        while True:
            rd1 = random.randint(0, len(self.procedural_objects)-1)
            obj1 = self.procedural_objects[rd1]
            #need to work on rules
            if obj1.type == 1:
                break
        
        while True:
            rd2 = random.randint(0, len(self.procedural_objects)-1)
            obj2 = self.procedural_objects[rd2]
            #need to work on rules
            if obj2.type == 1 and rd1 != rd2:
                break

        return (rd1, rd2)


def start_obj(start_pos, generic_object_list, start_type):

    cur_type = start_type
    start_scope = generic_object_list[cur_type].scope
    gen_hash = generic_object_list[cur_type].generate_hash()
    cur_obj = procedural_objects.Procedural_object(cur_type, start_pos, start_scope, gen_hash)
    cur_obj_x = cur_obj.length[0]
    cur_obj_y = cur_obj.length[1]
    cur_obj_z = cur_obj.length[2]
    update_pos = np.array([cur_obj_x, cur_obj_y, cur_obj_z])
    cur_obj.arbitrary_set_position(start_pos - update_pos)

    return cur_obj
