import generic_objects
import procedural_objects
import numpy as np

def execute_model(generic_object_list, start_obj, steps):
    production_list = []
    
    cur_obj = start_obj
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
        next_hash = next_generic_obj.generate_hash()
        next_obj = procedural_objects.Procedural_object(next_type, np.array([0,0,0]), next_scope, next_hash)
        next_choice = cur_generic_obj.execute_rule(next_type)
        cur_obj = production_list[tempt_count+1]
        cur_obj.add_connected(next_choice)
        next_obj.add_connected(opposite_direction(next_choice))
        next_obj.set_position(cur_obj, next_choice)

        production_list.append(next_obj)
        cur_obj = next_obj

        if next_generic_obj.canTerminate == "False":
            not_end = True
        else:
            not_end = False
    
        count += 1
    production_list.pop(0)
    return production_list

def execute_model_withDirection(objStart, generic_object_list, delta, direction, available_endings, objEnd):
    dummy_pos = np.array([0,0,0])
    production_list = []
    rules_list = []

    direction_idx = direction_to_index(direction)

    lower_bound = objStart.length[direction_idx]
    current_bound = objStart.length[direction_idx]
    upper_bound = objStart.length[direction_idx]

    prev_lower_bound = 0
    prev_current_bound = 0
    prev_upper_bound = 0

    current_type = objStart.type
    cur_obj = objStart
    # detla = update_delta(direction, delta, objStart)

    #execute rule to get the objects
    while True:
        current_generic_obj = generic_object_list[current_type]

        ok, next_type, rule_chosen = current_generic_obj.get_nextType_with_direction(direction)
        if ok != True:
            return (False, [])
        next_type = int(next_type)

        next_generic_obj = generic_object_list[next_type]
        next_scope = next_generic_obj.scope
        next_hash = next_generic_obj.generate_hash()
        next_obj = procedural_objects.Procedural_object(next_type, dummy_pos, next_scope, next_hash)
        cur_obj.add_connected(rule_chosen)
        next_obj.add_connected(opposite_direction(rule_chosen))
        production_list.append(next_obj)
        rules_list.append(rule_chosen)
        
        if direction_idx != 2:
            lower_bound += next_scope[direction_idx][0] + prev_lower_bound
            current_bound += next_obj.length[direction_idx] + prev_current_bound
            upper_bound += next_scope[direction_idx][1] + prev_upper_bound
            prev_lower_bound = next_scope[direction_idx][0]
            prev_current_bound = next_obj.length[direction_idx]
            prev_upper_bound = next_scope[direction_idx][1]
        elif objEnd.type == 3 or objEnd.type == 8:
            lower_bound += next_scope[direction_idx][0] + prev_lower_bound
            current_bound += next_obj.length[direction_idx] + prev_current_bound
            upper_bound += next_scope[direction_idx][1] + prev_upper_bound
            prev_lower_bound = next_scope[direction_idx][0]
            prev_current_bound = next_obj.length[direction_idx]
            prev_upper_bound = next_scope[direction_idx][1]
        else:
            lower_bound += next_scope[direction_idx][0] *2
            current_bound += next_obj.length[direction_idx] *2
            upper_bound += next_scope[direction_idx][1] *2

        current_type = next_type

        if upper_bound>delta[direction_idx] and lower_bound<delta[direction_idx] and valid_ending(available_endings, current_type):
            break
        
        if lower_bound > delta[direction_idx]:
            print("failed")
            return (False, [])

    #find exact scope of the objects
    if current_bound < delta[direction_idx]:
        production_list = add_scope(current_bound, delta, production_list, direction_idx)

    if current_bound > delta[direction_idx]:
        production_list = minus_scope(current_bound, delta, production_list, direction_idx)

    # production_list = adjust_scope(production_list)

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

def adjust_scope(production_list):
    target_adjust = production_list[-1].length[0]
    for obj in production_list:
        available_adjust =  (obj.length[0] - obj.scope[0][0]) * 2
        if target_adjust > available_adjust:
            obj.length[0] = obj.scope[0][0]
            target_adjust -= available_adjust
        else: 
            obj.length[0] -= target_adjust * 0.5
            break
    return production_list
       

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

def update_delta(direction, delta, start_obj):
    if direction == '+x' or direction == '-x':
        delta -= np.array([start_obj.length[0], 0, 0])
 
    if direction == '+y' or direction == '-y':
        delta -= np.array([0, start_obj.length[1], 0])

    if direction == '+z' or direction == '-z':
        delta -= np.array([0, 0, start_obj.length[2]])

def opposite_direction(direction):
    if direction == '+x':
        return '-x'
    if direction == '-x':
        return '+x'
    if direction == '+y':
        return '-y'
    if direction == '-y':
        return '+y'
    if direction == '+z':
        return '-z'
    if direction == '-z':
        return '+z'
    
    return '+x'