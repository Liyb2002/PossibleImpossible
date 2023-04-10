import generic_objects
import procedural_objects

def execute_model(start_pos, object_list):
    production_list = []

    cur_id = 1
    start_scope = object_list[cur_id].scope
    cur_obj = procedural_objects.Procedural_object(cur_id, start_pos, start_scope)
    production_list.append(cur_obj)

    #processing
    # count = 0
    while(True):
        cur_generic_obj = object_list[cur_id]
        next_id = cur_generic_obj.get_next()
        if next_id == None:
            break
        
        next_generic_obj = object_list[next_id]
        next_scope = next_generic_obj.scope
        next_obj = procedural_objects.Procedural_object(next_id, start_pos, next_scope)
        next_choice = cur_generic_obj.execute_rule(next_id)
        next_obj.set_position(cur_obj, next_choice)

        cur_id = next_id
        cur_obj = next_obj
        production_list.append(cur_obj)
    
    return production_list