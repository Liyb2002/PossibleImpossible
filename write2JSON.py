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
                'mode': '1'}
                    }
            self.result.append(data)

        with open(file_name, 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []


    def write_small_cubes(self, small_cube_list):
        for obj in small_cube_list:
            data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.length[0]),
                'scale_y': float(obj.length[1]),
                'scale_z': float(obj.length[2]),
                'mode': '1'}
                    }
            result.append(data)

    def write_skeleton(self, obj_list, file_name):
        for obj in obj_list:
            data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.length[0]),
                'scale_y': float(obj.length[1]),
                'scale_z': float(obj.length[2]),
                'mode': '1'}
                    }
            self.result.append(data)

        with open(file_name, 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []

    def write(self):
        with open('./three/result.json', 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []
