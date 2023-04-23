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


def execute_model_withDirection(objStart, generic_object_list, delta, direction, available_endings):
    dummy_pos = np.array([0,0,0])
    production_list = []
    rules_list = []

    lower_bound = 0
    current_bound = 0
    upper_bound = 0
    direction_idx = direction_to_index(direction)

    current_type = objStart.type

    #execute rule to get the objects
    while True:
        current_generic_obj = generic_object_list[current_type]

        next_type, rule_chosen = current_generic_obj.get_nextType_with_direction(direction)
        next_type = int(next_type)

        next_generic_obj = generic_object_list[next_type]
        next_scope = next_generic_obj.scope
        next_obj = procedural_objects.Procedural_object(next_type, dummy_pos, next_scope)
        production_list.append(next_obj)
        rules_list.append(rule_chosen)
        
        # print("upper_bound plus", next_scope[direction_idx][1])
        lower_bound += next_scope[direction_idx][0]*2
        current_bound += next_obj.length[direction_idx]*2
        upper_bound += next_scope[direction_idx][1]*2
        current_type = next_type

        if upper_bound>delta[direction_idx] and lower_bound<delta[direction_idx] and valid_ending(available_endings, current_type):
            break
        
        if lower_bound > delta[direction_idx]:
            print("failed")
            return (False, [])

    
    # print("delta", delta)
    # print("number of objects", len(production_list))
    # print("final lower_bound", lower_bound)
    # print("final current_bound", current_bound)
    # print("final upper_bound", upper_bound)
    # print("delta[direction_idx]", delta[direction_idx])

    #find exact scope of the objects
    if current_bound < delta[direction_idx]:
        production_list = add_scope(current_bound, delta, production_list, direction_idx)

    if current_bound > delta[direction_idx]:
        production_list = minus_scope(current_bound, delta, production_list, direction_idx)

    #set object positions
    first_obj = production_list[0]
    first_obj.set_position(objStart, rules_list[0])
    for i in range(1, len(production_list)):
        prev_obj = production_list[i-1]
        cur_obj = production_list[i]
        cur_obj.set_position(prev_obj, rules_list[i])

    return (True, production_list)
    
def add_scope(current_bound, delta, production_list, direction_idx):
    # print("do add scope")
    for obj in production_list:
        target_add = delta[direction_idx] - current_bound
        available_add = (obj.scope[direction_idx][1] - obj.length[direction_idx]) * 2
        if target_add > available_add:
            obj.length[direction_idx] = obj.scope[direction_idx][1]
            current_bound += available_add
        else:
            obj.length[direction_idx] += target_add * 0.5
            break
    return production_list

def minus_scope(current_bound, delta, production_list, direction_idx):
    # print("do minus scope")
    for obj in production_list:
        target_minus = current_bound - delta[direction_idx]
        available_minus = (obj.length[direction_idx] - obj.scope[direction_idx][0]) * 2
        if target_minus > available_minus:
            obj.length[direction_idx] = obj.scope[direction_idx][0]
            current_bound -= available_minus
        else:
            obj.length[direction_idx] -= target_minus * 0.5
            break
    return production_list

def start_obj(start_pos, generic_object_list, start_type):

    cur_type = start_type
    start_scope = generic_object_list[cur_type].scope
    cur_obj = procedural_objects.Procedural_object(cur_type, start_pos, start_scope)
    cur_obj_x = cur_obj.length[0]
    cur_obj_y = cur_obj.length[1]
    cur_obj_z = cur_obj.length[2]
    update_pos = np.array([cur_obj_x, cur_obj_y, cur_obj_z])
    cur_obj.arbitrary_set_position(start_pos - update_pos)

    return cur_obj

def direction_to_index(direction):
    if direction == '+x' or direction == '-x':
        return 0
    
    if direction == '+y' or direction == '-y':
        return 1
    
    return 2

def valid_ending(available_endings, cur_type):
    for ending in available_endings:
        if ending == cur_type:
            return True
    
    return False