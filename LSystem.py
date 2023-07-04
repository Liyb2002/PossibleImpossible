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
        self.rules = []
        self.light_pos = np.array([0.0,0.0,0.0])
        self.startpos = np.array([0.0,0.0,0.0])

        self.add_rule()
        self.init_state()
        self.run_system()

    def init_state(self):
        start_module = LModule.Module(self.startpos, np.array([0.2,0.03,0.03]), np.array([0,0,0]))
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
            self.new_objects += obj.execute(self.light_pos, self.rules)
            self.procedural_objects.append(obj.toProcedual())
    
    def add_rule(self):
        new_rule = rule(11)
        self.rules.append(new_rule)

    def finish_system(self):
        return self.procedural_objects


class rule:
    def __init__(self, left_hand_type):
        self.lhs_type = left_hand_type
        self.rhs_types = [11, 11]
        self.rhs_size_multiplier = [[0.8,0.8,0.8], [0.8,0.8,0.8]]
        self.rhs_rotations = [[0.0, 0.0, 0.2], [0.0, 0.0, -0.2]]
        self.rhs_offsets = [[0.15, 0.15, 0.0], [0.15, -0.15, 0.0]]
        self.rhs_directions = ["top", "bot"]
