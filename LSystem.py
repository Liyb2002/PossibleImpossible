import LModule
import procedural_objects

import json
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

        self.add_rules()
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
    
    def add_rules(self):
        with open('tree/LSystem.json', 'r') as object_file:
            rules_json = json.load(object_file)
            for rule_json in rules_json:
                new_rule = rule(rule_json)
                self.rules.append(new_rule)

    def finish_system(self):
        return self.procedural_objects


class rule:
    def __init__(self, rule_json):
        self.lhs_type = rule_json['lhs_type']
        self.rhs_types = rule_json['rhs_types']
        self.rhs_size_multiplier = rule_json['rhs_size_multiplier']
        self.rhs_rotations = rule_json['rhs_rotations']
        self.rhs_offsets = rule_json['rhs_offsets']
        self.rhs_directions = rule_json['rhs_directions']
