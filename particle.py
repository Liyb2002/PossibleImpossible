import produce
import cycle_connect

class Particle:
    def __init__(self, generic_object_list):
        self.generic_object_list = generic_object_list


    def run_particle(self,intersection, start_type, steps, isFront):
        if isFront:
            self.front_list = produce.execute_model(intersection, self.generic_object_list, start_type, steps)
        else:
            self.back_list = produce.execute_model(intersection, self.generic_object_list, start_type, steps)
        
    def run_connect(self):
        self.connect_list = cycle_connect.solve_3D(self.generic_object_list, self.front_list[-1], self.back_list[-1])
