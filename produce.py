import generic_objects
import procedural_objects
import numpy as np

def execute_model(start_pos, generic_object_list, start_type, steps):
    production_list = []
    
    cur_obj = start_obj(start_pos, generic_object_list, start_type)
    production_list.append(cur_obj)

    #processing
    count = 0
    not_end = True
    while(count < steps or not_end):

        tempt_count = count
        next_type = None

        while(tempt_count >= 0 and next_type == None):
            cur_type = production_list[tempt_count].type
            cur_generic_obj = generic_object_list[cur_type]
            next_type = cur_generic_obj.get_nextType()
            tempt_count -=1

        next_generic_obj = generic_object_list[next_type]
        next_scope = next_generic_obj.scope
        next_obj = procedural_objects.Procedural_object(next_type, start_pos, next_scope)
        next_choice = cur_generic_obj.execute_rule(next_type)
        cur_obj = production_list[tempt_count+1]
        next_obj.set_position(cur_obj, next_choice)

        production_list.append(next_obj)
        cur_obj = next_obj

        if next_generic_obj.canTerminate == "False":
            not_end = True
        else:
            not_end = False
    
        count += 1

    return production_list


def execute_model_withDirection(objStart, generic_object_list, delta, direction):
    dummy_pos = np.array([0,0,0])
    production_list = []

    lower_bound = 0
    current_bound = 0
    upper_bound = 0

    current_type = objStart.type

    #execute rule to get the objects
    while upper_bound< abs(delta[0]):
        current_generic_obj = generic_object_list[current_type]

        next_type = current_generic_obj.get_nextType_with_direction(direction)
        next_generic_obj = generic_object_list[next_type]
        next_scope = next_generic_obj.scope
        next_obj = procedural_objects.Procedural_object(next_type, dummy_pos, next_scope)
        production_list.append(next_obj)
        
        lower_bound += next_scope[0][0]
        current_bound += next_obj.len_x
        upper_bound += next_scope[0][1]
        current_type = next_type
    

    print("final lower_bound", lower_bound)
    print("final current_bound", current_bound)
    print("final upper_bound", upper_bound)
    print("delta[0]", delta[0])
    
    if lower_bound > delta[0]:
        print("failed")
        return

    #find exact scope of the objects
    if current_bound < delta[0]:
        production_list = add_scope(current_bound, delta, production_list)

    if current_bound > delta[0]:
        production_list = minus_scope(current_bound, delta, production_list)

    real_bound = 0
    for obj in production_list:
        real_bound += obj.len_x
    print("real_bound", real_bound)

def add_scope(current_bound, delta, production_list):
    print("do add scope")
    for obj in production_list:
        target_add = delta[0] - current_bound
        available_add = obj.scope[0][1] - obj.len_x
        if target_add > available_add:
            obj.len_x = obj.scope[0][1]
            current_bound += available_add
        else:
            obj.len_x += target_add
            break
    return production_list

def minus_scope(current_bound, delta, production_list):
    print("do minus scope")
    for obj in production_list:
        target_minus = current_bound - delta[0]
        available_minus = obj.len_x - obj.scope[0][0]
        if target_minus > available_minus:
            obj.len_x = obj.scope[0][0]
            current_bound -= available_minus
        else:
            obj.len_x -= target_minus
            break
    return production_list

def start_obj(start_pos, generic_object_list, start_type):

    cur_type = start_type
    start_scope = generic_object_list[cur_type].scope
    cur_obj = procedural_objects.Procedural_object(cur_type, start_pos, start_scope)
    cur_obj_x = cur_obj.len_x
    cur_obj_y = cur_obj.len_y
    cur_obj_z = cur_obj.len_z
    update_pos = np.array([cur_obj_x, cur_obj_y, cur_obj_z])
    cur_obj.arbitrary_set_position(start_pos - update_pos)

    return cur_obj

