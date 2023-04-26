import produce
import numpy as np

def solve_3D(generic_object_list, objStart, objEnd):
    startPos = objStart.position
    endPos = objEnd.position

    # print("startPos", startPos)
    # print("startlength", objStart.length)

    # print("endPos", endPos)
    # print("endlength", objEnd.length)

    delta = endPos - startPos

    production_list = solve_1D(generic_object_list, delta, objStart, objEnd)
    return production_list

def solve_1D(generic_object_list, delta, objStart, objEnd):

    production_list = []
    production_list.append(objStart)
    abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
    abs_delta -= np.array([0, 0, objEnd.length[2]])

    directions = get_dirs(delta)
    directions = update_order(objStart, directions)

    ok, new_production = single_execution(abs_delta, 0, generic_object_list, directions, production_list, objEnd, 0)
    if ok != True:
        return []
    production_list += new_production

    ok, new_production = single_execution(abs_delta, 1, generic_object_list, directions, production_list, objEnd, 1)
    if ok != True:
        return []
    production_list += new_production

    ok, new_production = single_execution(abs_delta, 2, generic_object_list, directions, production_list, objEnd, 2)
    if ok != True:
        return []
    production_list += new_production

    print("startPos", objStart.position)
    print("startType", objStart.type)
    print("startlength", objStart.length)

    print("endPos", objEnd.position)
    print("endType", objEnd.type)
    print("endlength", objEnd.length)

    for obj in production_list:
        print("-------------new obj-------------")
        print("type", obj.type)
        print(obj.position)
        print(obj.length)

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

def single_execution(abs_delta, index, generic_object_list, directions, production_list, objEnd, count):
    if abs_delta[index] != 0:
        available_endings = Available_Ending_With_Direction(generic_object_list, directions[index])

        if count == 2:
            available_endings = Available_Ending_With_Object(generic_object_list, objEnd)

        ok, production_list_1 = produce.execute_model_withDirection(production_list[-1], generic_object_list,abs_delta,directions[index],available_endings, objEnd)
        if ok != True:
            return (ok, [])

        return (ok, production_list_1)
