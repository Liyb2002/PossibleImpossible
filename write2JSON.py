import json

def write(production_list):
    with open('./result.json', 'w') as f:
        result = []
        
        for obj in production_list:
            pos = list(obj.position)
            data = {'obj':
                {'type': obj.type,
                'position_x': float(obj.position[0]),
                'position_y': float(obj.position[1]),
                'position_z': float(obj.position[2]),
                'scope_x': float(obj.scope[0]),
                'scope_y': float(obj.scope[1]),
                'scope_z': float(obj.scope[2])}
                }
            result.append(data)

        json.dump(result, f, indent=2)

