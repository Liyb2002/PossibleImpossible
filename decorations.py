import json
import numpy as np
import procedural_objects
import random

class decoration_operator:
    def __init__(self):
        self.generic_footprint_list = []
        self.generic_nonterminal_list = []
        self.generic_terminal_list = []

        self.read_decorations()

    def read_decorations(self):
        with open('decorate.json', 'r') as object_file:
            objects_data = json.load(object_file)

            new_object = generic_footprint_object(objects_data[0])
            self.generic_footprint_list.append(new_object)

            for object_data in objects_data:
                if (object_data["category"] == "footprint"):
                    new_object = generic_footprint_object(object_data)
                    self.generic_footprint_list.append(new_object)
                
                if (object_data["category"] == "nonterminal"):
                    new_object = generic_nonterminal_object(object_data)
                    self.generic_nonterminal_list.append(new_object)
                
                if (object_data["category"] == "terminal"):
                    new_object = generic_terminal_object(object_data)
                    self.generic_terminal_list.append(new_object)
    
    def decorate(self, procedural_objects):
        #go through all main objects produced
        instance_list = []

        for obj in procedural_objects:
            input_type = obj.type
            min_pos = obj.position - obj.length
            max_pos = obj.position + obj.length

            #if we have decoration for this main object
            for footprint_object in self.generic_footprint_list:
                if footprint_object.structural_id == input_type:
                    
                    #get a random subdivison rule
                    subdiv_rule = footprint_object.execute_subdiv()

                    #execute the subdivision rule
                    total_nonterminal_list, total_terminal_list = self.parse_rule(subdiv_rule, min_pos, max_pos)

                    while len(total_nonterminal_list) > 0:
                        nonterminal_obj = total_nonterminal_list[-1]
                        total_nonterminal_list.pop()

                        generic_nonterminal_object = self.generic_nonterminal_list[obj.type]
                        subdiv_rule = generic_nonterminal_object.execute_subdiv()
                        tempt_nonterminal_list, tempt_terminal_list = self.parse_rule(subdiv_rule, min_pos, max_pos)
                        
                        total_terminal_list += tempt_terminal_list
                        total_nonterminal_list += tempt_nonterminal_list

                    instance_list += total_terminal_list
        
        return instance_list

    # def terminals_output(self, instance_list):
    #     for obj in instance_list:
    #         cur_type = obj.type
    #         generic_terminal_object = self.generic_terminal_list[cur_type]
    #         multiplier = generic_terminal_object.multiplier


    def parse_rule(self, subdiv_rule, min_pos, max_pos):
        split_dir = subdiv_rule[1]
        scope = max_pos - min_pos
        culmulative_percentage = 0

        nonterminal_list = []
        terminal_list = []

        if split_dir == "y direction":
            for i in range(2, len(subdiv_rule)):
                new_obj_info = subdiv_rule[i]
                tempt_min_pos = min_pos + np.array([0, culmulative_percentage * scope[1], 0])
                tempt_max_pos = np.array([max_pos[0], tempt_min_pos[1] + new_obj_info[2]*scope[2], max_pos[2]])
                culmulative_percentage += new_obj_info[2]

                if new_obj_info[0] == "nonterminal":
                    new_instance_nonterminal_object = instance_nonterminal_object(new_obj_info[1], tempt_min_pos, tempt_max_pos)
                    nonterminal_list.append(new_instance_nonterminal_object)

                if new_obj_info[0] == "terminal":
                    new_instance_terminal_object = instance_terminal_object(new_obj_info[1], tempt_min_pos, tempt_max_pos)
                    generic_terminal_object = self.generic_terminal_list[int(new_instance_terminal_object.type)]
                    multiplier = generic_terminal_object.multiplier
                    new_instance_terminal_object.set_position((tempt_min_pos+tempt_max_pos)*0.5)
                    new_instance_terminal_object.set_size((tempt_max_pos-tempt_min_pos)*0.5 * multiplier)
                    terminal_list.append(new_instance_terminal_object)
                
        return (nonterminal_list, terminal_list)

class generic_footprint_object:
    def __init__(self, info):
        self.structural_id = info['structural_id']
        self.subdiv = info['subdiv']

    def execute_subdiv(self):
        seed = random.uniform(0, 1)
        culmulative_prob = 0

        for subdiv_rule in self.subdiv:
            culmulative_prob += subdiv_rule[0]
            if culmulative_prob >= seed:
                break
        
        return subdiv_rule

class generic_nonterminal_object:
    def __init__(self, info):
        self.nonterminal_id = info['nonterminal_id']
        self.subdiv = info['subdiv']

    def execute_subdiv(self):
        seed = random.uniform(0, 1)
        culmulative_prob = 0

        for subdiv_rule in self.subdiv:
            culmulative_prob += subdiv_rule[0]
            if culmulative_prob >= seed:
                break
        
        return subdiv_rule


class generic_terminal_object:
    def __init__(self, info):
        self.terminal_id = info['terminal_id']
        self.rule = info['rule']
        self.multiplier = info['multiplier']

class instance_nonterminal_object:
    def __init__(self, type, min_pos, max_pos):
        self.type = type
        self.min_pos = min_pos
        self.max_pos = max_pos


class instance_terminal_object:
    def __init__(self, type, min_pos, max_pos):
        self.type = type
        self.min_pos = min_pos
        self.max_pos = max_pos
    
    def set_position(self, position):
        self.position = position

    def set_size(self, size):
        self.size = size 
