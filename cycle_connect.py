import produce
import numpy as np

def solve_3D(generic_object_list, objStart, objEnd):
    startPos = objStart.position
    endPos = objEnd.position

    delta = endPos - startPos
    print("delta", delta)

    production_list = solve_1D(generic_object_list, delta, objStart)
    return production_list

def solve_1D(generic_object_list, delta, objStart):

    abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])

    if delta[0] > 0:
        production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"+x")
    elif delta[0] < 0:
        production_list = produce.execute_model_withDirection(objStart, generic_object_list,abs_delta,"-x")

    return production_list