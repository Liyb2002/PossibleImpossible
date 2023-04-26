import produce
import cycle_connect

class Particle:
    def __init__(self, generic_object_list):
        self.generic_object_list = generic_object_list
        self.success = True
        self.procedural_objects = []


    def run_particle(self,intersection, start_type, steps, isFront):
        if isFront:
            self.procedural_objects += produce.execute_model(intersection, self.generic_object_list, start_type, steps)
            self.start = self.procedural_objects[-1]
        else:
            self.procedural_objects += produce.execute_model(intersection, self.generic_object_list, start_type, steps)
            self.end = self.procedural_objects[-1]

    def run_connect(self):
        # ending = self.find_connect_ending()
        self.connect_list = cycle_connect.solve_3D(self.generic_object_list, self.start, self.end)
        if len(self.connect_list) == 0:
            print("failed particle")
            self.success = False
        self.procedural_objects += self.connect_list
    
    def overlapping_check(self):
        for obj_A in self.connect_list:
            for obj_B in self.procedural_objects:
                overlapping = obj_A.collision_check(obj_B)
                if overlapping:
                    self.success = False
            
    def find_connect_ending(self):
        for obj in self.back_list:
            if obj.type == 1:
                print("obj.type", obj.type)
                return obj