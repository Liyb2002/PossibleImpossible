import json
import numpy as np


class decoration_operator:
    def __init__(self):
        self.main_decoration_list = []
        self.sub_decoration_list = []
        self.sub_decorations = {}
        self.prepare_subdivs()

        self.read_decorations()
        self.sort_decorations()

    def read_decorations(self):
        with open('decorate.json', 'r') as object_file:
            objects_data = json.load(object_file)

            new_object = main_decoration_object(objects_data[0])
            self.main_decoration_list.append(new_object)

            for object_data in objects_data:
                if (object_data["is_main"] == "True"):
                    new_object = main_decoration_object(object_data)
                    self.main_decoration_list.append(new_object)
                else:
                    new_object = sub_decoration_object(object_data)
                    self.sub_decoration_list.append(new_object)

    def sort_decorations(self):
        for obj in self.main_decoration_list:
            self.sub_decorations[obj.structural_id] = {}
            for subdiv in self.subdiv_list:
                self.sub_decorations[obj.structural_id][subdiv] = []
        
        for obj in self.sub_decoration_list:
            self.sub_decorations[obj.main_id][obj.subdiv].append(obj)
    
    def get_decorations(self, main_obj):
        structural_id = main_obj.structural_id
        return self.sub_decorations[structural_id]

    def decorate(self, procedural_objects):
        #go through all main objects produced
        for obj in procedural_objects:
            target_type = obj.type

            #if we have decoration for this main object
            if target_type in self.sub_decorations:

                #go through all its possible subdivisions
                for subdiv in self.subdiv_list:
                    possible_decorations = self.sub_decorations[target_type][subdiv]

                    #if we have decorations for this subdivision, pick an decoration
                    if len(possible_decorations) > 0:
                        decorate_obj = possible_decorations[-1]
                        self.execute_decorations(obj, decorate_obj)
    
    def execute_decorations(self, main_obj, decorate_obj):
        rule = decorate_obj.rule
        if rule == "center":
            print("center rule!")

    
    def prepare_subdivs(self):
        self.subdiv_list = ["top", "bot", "left", "right", "front", "back"]


class main_decoration_object:
    def __init__(self, info):
        self.structural_id = info['structural_id']


class sub_decoration_object:
    def __init__(self, info):
        self.main_id = info['main_id']
        self.sub_id = info['sub_id']
        self.subdiv = info['subdiv']
        self.rule = info['rule']
        self.set_scope(info)

    def set_scope(self, info):
        scope_x = info['scope_x']
        scope_y = info['scope_y']
        scope_z = info['scope_z']
        self.scope = np.array([scope_x,scope_y,scope_z])
