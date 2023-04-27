import produce
import cycle_connect
import random

class Particle:
    def __init__(self, generic_object_list):
        self.generic_object_list = generic_object_list
        self.success = True
        self.procedural_objects = []


    def run_particle(self,intersection, start_type, steps, isFront):
        if isFront:
            self.procedural_objects += produce.execute_model(intersection, self.generic_object_list, start_type, steps)
        else:
            self.procedural_objects += produce.execute_model(intersection, self.generic_object_list, start_type, steps)

    def run_connect(self):
        connect_list = cycle_connect.solve_3D(self.generic_object_list, self.procedural_objects[-1], self.procedural_objects[0])
        if len(connect_list) == 0:
            print("failed particle")
            self.success = False
        self.procedural_objects += connect_list
    
    def run_particle2(self, steps):
        rd1, rd2 = self.random_object()
        objStart = self.procedural_objects[rd1]
        objStart2 = self.procedural_objects[rd2]

        self.procedural_objects += produce.execute_model2(self.generic_object_list, objStart, steps)
        self.procedural_objects += produce.execute_model2(self.generic_object_list, objStart2, steps)

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