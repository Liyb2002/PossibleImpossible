import produce

def solve_3D(generic_object_list, objStart, objEnd):
    startPos = objStart.position
    endPos = objEnd.position

    delta = endPos - startPos
    print("delta", delta)

    solve_1D(generic_object_list, delta, objStart)

def solve_1D(generic_object_list, delta, objStart):
    produce.execute_model_withDirection(objStart, generic_object_list,delta,"x")
