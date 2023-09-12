import LSystem
import numpy as np
import decorations

def initSystem(decorate_path):
    print("hello")

    start_pos = np.array([2,2,2])
    rotation = np.array([0,0,0])
    group_count = 1
    light_pos = np.array([5,5,5])

    system = LSystem.LSys()
    system.system_setup(start_pos, rotation, group_count, light_pos)
    system.run_system()
    L_backbone = system.finish_system()

    decorator = decorations.decoration_operator(decorate_path)
    decoration_list = decorator.decorate(L_backbone)
    return decoration_list

