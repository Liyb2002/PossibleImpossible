import produce
import numpy as np

def solve_3D(generic_object_list, objStart, objEnd):
    startPos = objStart.position
    endPos = objEnd.position

    delta = endPos - startPos
    delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
    print("delta", delta)

    solve_1D(generic_object_list, delta, objStart)

def solve_1D(generic_object_list, delta, objStart):
    produce.execute_model_withDirection(objStart, generic_object_list,delta,"+x")
