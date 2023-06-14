import json


class output:
    def __init__(self):
        self.result = []    
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

    def write_small_cubes(self, small_cube_list):
        small_cubes = []
        print("len(small_cube_list)", len(small_cube_list))
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
            small_cubes.append(data)

        with open('./three/result.json', 'w') as f:
            json.dump(small_cubes, f, indent=2)

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
