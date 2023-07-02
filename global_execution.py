import copy
import random
import numpy as np
import procedural_objects

def global_assign(procedural_objects_list, global_objects):
    for global_object in global_objects:
        action = global_object['action']
        if action[0] == 'assign':
            procedural_objects_list = action_assign(procedural_objects_list, global_object)
        if action[0] == 'add':
            procedural_objects_list = action_add(procedural_objects_list, global_object)

    return procedural_objects_list

def action_assign(procedural_objects_list, global_object):
    for obj in procedural_objects_list:
        
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
    
    return procedural_objects_list

def action_add(procedural_objects_list, global_object):
    min_x = 100
    max_x = -100
    min_y = 100
    max_y = -100
    min_z = 100
    max_z = -100

    for obj in procedural_objects_list:

        if min_x > obj.position[0] - obj.length[0]:
            min_x = obj.position[0] - obj.length[0]
        if max_x < obj.position[0] + obj.length[0]:
            max_x = obj.position[0] + obj.length[0]

        if min_y > obj.position[1] - obj.length[1]:
            min_y = obj.position[1] - obj.length[1]
        if max_y < obj.position[1] + obj.length[1]:
            max_y = obj.position[1] + obj.length[1]

        if min_z > obj.position[2] - obj.length[2]:
            min_z = obj.position[2] - obj.length[2]
        if max_z < obj.position[2] + obj.length[2]:
            max_z = obj.position[2] + obj.length[2]


    dummy_scope = [0.1, 0.1]
    obj_xpos = 0.0
    obj_ypos = 0.0
    obj_zpos = 0.0
    obj_sizeX = 0.0
    obj_sizeY = 0.0
    obj_sizeZ = 0.0

    if global_object['pos'][0][0] == "middle":
        obj_xpos = (min_x+max_x) / 2.0
    
    if global_object['pos'][1][0] == "top":
        obj_ypos = max_y + global_object['pos'][1][1]

    if global_object['pos'][1][0] == "bot":
        obj_ypos = min_y - global_object['pos'][1][1]

    if global_object['pos'][2][0] == "middle":
        obj_zpos =  (min_z+max_z) / 2.0

    if global_object['size'][0][0] == "mult":
        obj_sizeX = (max_x - min_x) * global_object['size'][0][1]

    if global_object['size'][1][0] == "fixed":
        obj_sizeY = global_object['size'][1][1]

    if global_object['size'][2][0] == "mult":
        obj_sizeZ = (max_z - min_z) * global_object['size'][2][1]

    tempt_obj = procedural_objects.Procedural_object(global_object['object_id'], np.array([obj_xpos,obj_ypos,obj_zpos]), np.array([dummy_scope,dummy_scope,dummy_scope]), "00000", np.array([[0],[0],[0]]), np.array([0,0,0]))
    tempt_obj.arbitrary_set_length(np.array([float(obj_sizeX),float(obj_sizeY),float(obj_sizeZ)]))

    procedural_objects_list.append(tempt_obj)
    return procedural_objects_list


