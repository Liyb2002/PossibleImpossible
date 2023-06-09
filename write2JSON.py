import json


class output:
    def __init__(self):
        self.result = []   

    def write_result (self, decoration_list, file_name):
        for obj in decoration_list:
            pos = list(obj.position)
            data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.size[0]),
                'scale_y': float(obj.size[1]),
                'scale_z': float(obj.size[2]),
                'rotation_x' : float(obj.rotation[0]),
                'rotation_y' : float(obj.rotation[1]),
                'rotation_z' : float(obj.rotation[2]),
                'group': float(obj.group)}
                    }
            self.result.append(data)

        with open(file_name, 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []
    
    def write_proceudral_objects (self, proceudral_objects, file_name):
        for obj in proceudral_objects:
            pos = list(obj.position)
            data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.length[0]),
                'scale_y': float(obj.length[1]),
                'scale_z': float(obj.length[2]),
                'rotation_x' : float(obj.rotation[0]),
                'rotation_y' : float(obj.rotation[1]),
                'rotation_z' : float(obj.rotation[2]),
                'group': float(obj.group)}
                    }
            self.result.append(data)

        with open(file_name, 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []