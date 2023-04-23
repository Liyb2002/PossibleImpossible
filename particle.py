import produce
import cycle_connect

class Particle:
    def __init__(self, generic_object_list):
        self.generic_object_list = generic_object_list
        self.success = True


    def run_particle(self,intersection, start_type, steps, isFront):
        if isFront:
            self.front_list = produce.execute_model(intersection, self.generic_object_list, start_type, steps)
        else:
            self.back_list = produce.execute_model(intersection, self.generic_object_list, start_type, steps)
        
    def run_connect(self):
        self.connect_list = cycle_connect.solve_3D(self.generic_object_list, self.front_list[-1], self.back_list[-1])
        if len(self.connect_list) == 0:
            print("failed particle")
            self.success = False
    
    def overlapping_check(self):
        for obj_A in self.connect_list:
            for obj_B in self.front_list:
                overlapping = obj_A.collision_check(obj_B)
                if overlapping:
                    self.success = False
            
            for obj_B in self.back_list:
                overlapping = obj_A.collision_check(obj_B)
                if overlapping:
                    self.success = False

  