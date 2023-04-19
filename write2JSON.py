import json


class output:
    def __init__(self):
        self.result = []

    def prepare_write(self, production_list):
        for obj in production_list:
            pos = list(obj.position)
            data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.length[0]),
                'scale_y': float(obj.length[1]),
                'scale_z': float(obj.length[2]),
                'mode': '0'}
                    }
            self.result.append(data)

    def prepare_write_debug(self, production_list):
        count = 0
        for obj in production_list:
            pos = list(obj.position)
            count += 1
            if count == len(production_list):
                data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.length[0]),
                'scale_y': float(obj.length[1]),
                'scale_z': float(obj.length[2]),
                'mode': '0'}
                    }
            else:
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

    def write(self):
        with open('./three/result.json', 'w') as f:
            json.dump(self.result, f, indent=2)


