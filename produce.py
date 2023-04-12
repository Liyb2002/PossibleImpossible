import generic_objects
import procedural_objects
import numpy as np

def execute_model(start_pos, object_list, start_type, steps):
    production_list = []
    
    cur_obj = start_obj(start_pos, object_list, start_type)
    production_list.append(cur_obj)

    #processing
    count = 0
    not_end = True
    while(count < steps or not_end):

        tempt_count = count
        next_type = None

        while(tempt_count >= 0 and next_type == None):
            cur_type = production_list[tempt_count].type
            cur_generic_obj = object_list[cur_type]
            next_type = cur_generic_obj.get_next()
            tempt_count -=1

        print("next_type", next_type)
        next_generic_obj = object_list[next_type]
        next_scope = next_generic_obj.scope
        next_obj = procedural_objects.Procedural_object(next_type, start_pos, next_scope)
        next_choice = cur_generic_obj.execute_rule(next_type)
        cur_obj = production_list[tempt_count+1]
        next_obj.set_position(cur_obj, next_choice)

        cur_obj = next_obj
        production_list.append(cur_obj)

        if next_generic_obj.canTerminate == "False":
            not_end = True
        else:
            not_end = False
    
        count += 1

    return production_list

def start_obj(start_pos, object_list, start_type):

    cur_type = start_type
    start_scope = object_list[cur_type].scope
    cur_obj = procedural_objects.Procedural_object(cur_type, start_pos, start_scope)
    cur_obj_x = cur_obj.len_x
    cur_obj_y = cur_obj.len_y
    cur_obj_z = cur_obj.len_z
    update_pos = np.array([cur_obj_x, cur_obj_y, cur_obj_z])
    cur_obj.arbitrary_set(start_pos - update_pos)

    return cur_obj
