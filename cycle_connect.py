import produce
import numpy as np

def solve_3D(generic_object_list, objStart, objEnd):
    startPos = objStart.position
    endPos = objEnd.position

    print("startPos", startPos)
    print("startlength", objStart.length)

    print("endPos", endPos)
    print("endlength", objEnd.length)

    delta = endPos - startPos

    production_list = solve_1D(generic_object_list, delta, objStart, objEnd)
    return production_list

def solve_1D(generic_object_list, delta, objStart, objEnd):

    abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
    abs_delta -= np.array([0, 0, objEnd.length[2]])

    directions = get_dirs(delta)

    available_endings = Available_Ending_With_Direction(generic_object_list, directions[0])
    work_1, production_list_1 = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,directions[0],available_endings)
    if work_1 != True:
        return []

    available_endings = Available_Ending_With_Direction(generic_object_list, directions[1])
    work_2, production_list_2 = produce.execute_model_withDirection(production_list_1[-1], generic_object_list,abs_delta,directions[1],available_endings)
    if work_2 != True:
        return []

    available_endings = Available_Ending_With_Object(generic_object_list, objEnd)
    work_3, production_list_3 = produce.execute_model_withDirection(production_list_2[-1], generic_object_list,abs_delta,directions[2],available_endings)
    if work_3 != True:
        return []

    production_list = production_list_1 + production_list_2 + production_list_3
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
    
    print("possible_endings", possible_endings)
    return possible_endings

def get_dirs(delta):
    directions = []
    if delta[0] > 0:
        directions.append("+x")
    if delta[0] < 0:
        directions.append("-x")
    if delta[1] > 0:
        directions.append("+y")
    if delta[1] < 0:
        directions.append("-y")
    if delta[2] > 0:
        directions.append("+z")
    if delta[2] < 0:
        directions.append("-z")
    
    return directions