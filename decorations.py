import json


def read_decorations():
    main_decoration_list = []
    sub_decoration_list = []

    with open('decorate.json', 'r') as object_file:
        objects_data = json.load(object_file)

        main_decoration_list.append(object_data[0])
        for object_data in objects_data:
            if (object_data["is_main"] == "True"):
                new_object = main_decoration_object(object_data)
                main_decoration_list.append(new_object)
            else:
                new_object = sub_decoration_object(object_data)
                sub_decoration_list.append(new_object)

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
