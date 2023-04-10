import json

def write(production_list):
    with open('./three/result.json', 'w') as f:
        result = []
        
        for obj in production_list:
            pos = list(obj.position)
            data = {'obj':
                {'type': obj.type,
                'start_x': float(obj.position[0]),
                'start_y': float(obj.position[1]),
                'start_z': float(obj.position[2]),
                'scale_x': float(obj.scope[0]),
                'scale_y': float(obj.scope[1]),
                'scale_z': float(obj.scope[2])}
                }
            result.append(data)

        json.dump(result, f, indent=2)

