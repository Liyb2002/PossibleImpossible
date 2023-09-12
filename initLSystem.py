import LSystem
import numpy as np
import decorations
import json

def initSystem(decorate_path):
    print("hello")

    start_pos = np.array([0,-2,0])
    rotation = np.array([0,0,1.6])
    group_count = 1
    light_pos = np.array([5,5,5])

    system = LSystem.LSys()
    system.system_setup(start_pos, rotation, group_count, light_pos, init_size = np.array([1.0,0.1,0.1]))
    system.run_system()
    L_backbone = system.finish_system()

    decorator = decorations.decoration_operator(decorate_path)
    decoration_list = decorator.decorate(L_backbone)
    write_group(start_pos, rotation)

    print("len decorate list", len(decoration_list))
    return decoration_list

def write_group(start_pos, rotation):
    system_data = []
    data = {'System':
    {'group': 1,
    'origin_x': float(start_pos[0]),
    'origin_y': float(start_pos[1]),
    'origin_z': float(start_pos[2]),
    'system_rotation_x': float(rotation[0]),
    'system_rotation_y': float(rotation[1]),
    'system_rotation_z' : float(rotation[2])
        }
    }
    system_data.append(data)


    with open("three/system.json", 'w') as f:
        json.dump(system_data, f, indent=2)


