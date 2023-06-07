import json


class output:
    def __init__(self):
        self.result = []

    def edit_skeleton(self, production_list):
        for obj in production_list:
            if obj.type == 1:
                obj.length[0] = obj.length[0] * 1.2
                obj.length[1] = obj.length[1] * 1.2
                obj.length[2] = obj.length[2] * 1.2
            
            if obj.type == 4 or obj.type == 5 or obj.type == 6 or obj.type == 7:
                obj.length[1] = obj.length[1] * 0.2

            if obj.type == 3 or obj.type == 5:
                obj.length[0] = obj.length[0] * 0.8
                obj.length[2] = obj.length[2] * 0.8

    def prepare_write_skeleton(self, production_list):
        self.edit_skeleton(production_list)
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
    
    def prepare_write_decorations(self, decoration_list):
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

    def write(self):
        with open('./three/result.json', 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []


    def write_phase1(self):
        with open('./three/phase1.json', 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []
    
    def write_phase2(self):
        with open('./three/phase2.json', 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []

    def write_phase3(self):
        with open('./three/phase3.json', 'w') as f:
            json.dump(self.result, f, indent=2)
            self.result = []
