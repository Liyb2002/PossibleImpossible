import copy
import random
import numpy as np

def global_assign(procedural_objects, global_objects):
    for global_object in global_objects:
        action = global_object['action']
        if action[0] == 'assign':
            procedural_objects = action_assign(procedural_objects, global_object)

    return procedural_objects

def action_assign(procedural_objects, global_object):
    for obj in procedural_objects:
        
        if obj.type == global_object['prev_type']:
            assign_available = True
            for dir in obj.connected:
                if dir == global_object['prev_condition'][0]:
                    assign_available = False
            
            if assign_available:
                offset_x = random.uniform(global_object['offsets'][0][0],global_object['offsets'][0][1])
                offset_y = random.uniform(global_object['offsets'][1][0],global_object['offsets'][1][1])
                offset_z = random.uniform(global_object['offsets'][2][0],global_object['offsets'][2][1])

                obj.position += np.array([offset_x, offset_y, offset_z])
                obj.length += np.array([offset_x, offset_y, offset_z])
                obj.type = global_object['object_id']
    
    return procedural_objects



