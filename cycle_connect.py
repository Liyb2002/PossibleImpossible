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
    abs_delta -= objStart.length
    abs_delta -= objEnd.length

    print("abs_delta", abs_delta)

    if delta[1] > 0:
        production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"+y")
    elif delta[1] < 0:
        production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"-y")

    # if delta[0] > 0:
    #     production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"+x")
    # elif delta[0] < 0:
    #     production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"-x")
    
    # if delta[2] > 0:
    #     production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"+z")
    # elif delta[2] < 0:
    #     production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"-z")

    for obj in production_list:
        print("new obj")
        print(obj.position)
        print(obj.length)

    return production_list