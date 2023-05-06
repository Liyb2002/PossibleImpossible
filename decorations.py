import json
import numpy as np
import procedural_objects
import random

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
        instance_list = []

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
                        instance_list.append(self.execute_decorations(subdiv, obj, decorate_obj))

        return instance_list
        
    def execute_decorations(self, subdiv, main_obj, decorate_obj):
        rule = decorate_obj.rule

        decorate_obj_size = decorate_obj.return_length()
        decorate_obj_startPos = self.subdivs_to_pos(subdiv, main_obj, decorate_obj_size)
        decorate_obj_type = decorate_obj.main_id + 0.01*decorate_obj.sub_id

        if rule == "center":
            #create a new procedural object
            # print("startPos", decorate_obj_startPos)
            # print("center rule!")
            # print("main_obj center", main_obj.position)
            # print("main_obj scope", main_obj.length)
            new_decoration_object_instance = decoration_object_instance(decorate_obj_type, decorate_obj_startPos, decorate_obj_size)
            return new_decoration_object_instance
    
    def prepare_subdivs(self):
        self.subdiv_list = ["top", "bot", "left", "right", "front", "back"]

    def subdivs_to_pos(self, subdiv, main_obj, decorate_obj_size):
        position = main_obj.position
        length = main_obj.length
        add = np.array([0, 0, 0])
        
        if subdiv == "top":
            add = np.array([0, length[1] + decorate_obj_size[1], 0])
        if subdiv == "bot":
            add = np.array([0, -length[1] - decorate_obj_size[1], 0])
        if subdiv == "left":
            add = np.array([-length[0]-decorate_obj_size[0], 0, 0])
        if subdiv == "right":
            add = np.array([length[0]+decorate_obj_size[0],0, 0])
        if subdiv == "front":
            add = np.array([0, 0, length[2]+decorate_obj_size[2]])
        if subdiv == "back":
            add = np.array([0, 0,  -length[2]-decorate_obj_size[2]])
        
        return position + add

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
        self.scope_x = info['scope_x']
        self.scope_y = info['scope_y']
        self.scope_z = info['scope_z']
    
    def return_length(self):
        len_x = round(random.uniform(self.scope_x[0], self.scope_x[1]),4)
        len_y = round(random.uniform(self.scope_y[0], self.scope_y[1]),4)
        len_z = round(random.uniform(self.scope_z[0], self.scope_z[1]),4)
        length = np.array([len_x, len_y, len_z])
        return length

class decoration_object_instance:
    def __init__(self, type, position, size):
        self.type = type
        self.position = position
        self.size = size
