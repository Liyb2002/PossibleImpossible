import json
import numpy as np


class decoration_operator:
    def __init__(self):
        self.main_decoration_list = []
        self.sub_decoration_list = []
        self.sub_decorations = {}
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
            self.sub_decorations[obj.structural_id] = []

        for obj in self.sub_decoration_list:
            self.sub_decorations[obj.main_id].append(obj)
    
    def get_decorations(self, main_obj):
        structural_id = main_obj.structural_id
        results = []
        print(self.sub_decorations[structural_id])



class main_decoration_object:
    def __init__(self, info):
        self.structural_id = info['structural_id']
        self.subdiv = info['subdiv']



class sub_decoration_object:
    def __init__(self, info):
        self.main_id = info['main_id']
        self.sub_id = info['sub_id']
        self.rule = info['rule']
        self.set_scope(info)

    def set_scope(self, info):
        scope_x = info['scope_x']
        scope_y = info['scope_y']
        scope_z = info['scope_z']
        self.scope = np.array([scope_x,scope_y,scope_z])
