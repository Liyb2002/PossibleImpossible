import produce
import numpy as np
import random

def solve_1D(generic_object_list, objStart, objEnd):
    startPos = objStart.position
    endPos = objEnd.position

    delta = endPos - startPos

    production_list = []
    production_list.append(objStart)
    abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
    abs_delta -= np.array([0, 0, objEnd.length[2]])

    directions = get_dirs(delta)
    directions = update_order(objStart, directions)

    orders = random_order()
    for i in range(0,3):
        ok, new_production = single_execution(abs_delta, orders[i], generic_object_list, directions, production_list, objEnd, i)
        if ok != True:
            return []
        production_list += new_production

    return production_list

def Available_Ending_With_Object(generic_object_list, target_obj):
    possible_endings = []
    for i in range(1, len(generic_object_list)):
        for connect_id in generic_object_list[int(i)].connect_id:
            if connect_id == target_obj.type:
                possible_endings.append(i)
    
    return possible_endings

def Available_Ending_With_Direction(generic_object_list, direction):
    possible_endings = []
    for i in range(1, len(generic_object_list)):
        if generic_object_list[i].able_next_direction(direction):
            possible_endings.append(i)
    
    return possible_endings

def get_dirs(delta):
    directions = []
    if delta[0] > 0:
        directions.append("+x")
    if delta[0] <= 0:
        directions.append("-x")
    if delta[1] > 0:
        directions.append("+y")
    if delta[1] <= 0:
        directions.append("-y")
    if delta[2] > 0:
        directions.append("+z")
    if delta[2] <= 0:
        directions.append("-z")
    
    return directions

def update_order(objStart, directions):
    if objStart.arriving_rule == "+x" or objStart.arriving_rule == "-x":
        tempt_dir = directions[0]
        directions[0] = directions[1]
        directions[1] = tempt_dir
    
    return directions

def random_order():
    orders = []
    first = random.randint(0, 1)
    second = (first +1)%2
    third = 2

    orders.append(first)
    orders.append(second)
    orders.append(third)
    return orders

def single_execution(abs_delta, index, generic_object_list, directions, production_list, objEnd, count):

    if abs_delta[index] != 0:
        available_endings = Available_Ending_With_Direction(generic_object_list, directions[index])

        if count == 2:
            available_endings = Available_Ending_With_Object(generic_object_list, objEnd)

        connect_particle = produce.connect_execution(production_list[-1], generic_object_list,abs_delta,directions[index],available_endings, objEnd)
        ok = 1

        while ok == 1:
            ok = connect_particle.execute_model_withDirection()
        
        if ok == 0:
            return (False, [])
        
        if ok == 2:
            return (True, connect_particle.set_scope())
    
    return (True, [])
