import LSystem
import numpy as np
import decorations
import json
import write2JSON
import reduceDuplicate

def initSystem(decorate_path):
    print("hello")

    start_pos = np.array([0,-2,0])
    rotation = np.array([0,0,1.6])
    group_count = 1
    light_pos = np.array([5,5,5])

    system = LSystem.LSys()
    system.system_setup(start_pos, rotation, group_count, light_pos, sys_path = 'multiTree/backbone.json', init_size = np.array([2.0,0.2,0.2]))
    system.run_system()
    L_backbone = system.finish_system()


    output_writer = write2JSON.output()
    inner_matryoshka = []

    for obj in L_backbone:
        if obj.type == 13:
            inner_matryoshka.append(obj)
    
    inner_matryoshka = reduceDuplicate.reduce(inner_matryoshka)
    output_writer.write_proceudral_objects(inner_matryoshka, './inner_layer.json')

    decorator = decorations.decoration_operator(decorate_path)
    decoration_list = decorator.decorate(L_backbone)
    write_group(start_pos, rotation)

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


