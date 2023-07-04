import LModule
import procedural_objects

import numpy as np

class LSys:
    def __init__(self):
        self.alpha = 0.4
        self.min_light = 0.1
        self.max_age = 5
        self.bounding_box = np.array([[0.0,0.0], [0.0,0.0], [0.0,0.0]])
        self.steps = 4
        self.procedural_objects = []
        self.new_objects = []
        self.light_pos = np.array([0.0,0.0,0.0])
        self.startpos = np.array([0.0,0.0,0.0])

        self.init_state()
        self.run_system()

    def init_state(self):
        start_module = LModule.Module(self.startpos, np.array([0.1,0.05,0.05]))
        self.new_objects.append(start_module)
    
    def run_system(self):
        for i in range(0, self.steps):
            self.run_step()

    def run_step(self):

        level_count = len(self.new_objects)
        count = 1
        for obj in self.new_objects:
            if count > level_count:
                break
            count += 1
            self.new_objects.append(obj.execute(self.light_pos))
            self.procedural_objects.append(obj.toProcedual())
    
    def finish_system(self):
        return self.procedural_objects