import generic_objects
import procedural_objects

def execute_model(start_pos, object_list, start_id, steps):
    production_list = []
    cur_id = start_id

    start_scope = object_list[cur_id].scope
    cur_obj = procedural_objects.Procedural_object(cur_id, start_pos, start_scope, cur_id)
    production_list.append(cur_obj)

    #processing
    count = 0
    while(count < steps):

        tempt_count = count
        cur_id = production_list[tempt_count].id
        cur_generic_obj = object_list[cur_id]
        next_id = cur_generic_obj.get_next()

        while(tempt_count > 0 and next_id == None):
            tempt_count -=1
            cur_id = production_list[tempt_count].id
            cur_generic_obj = object_list[cur_id]
            next_id = cur_generic_obj.get_next()

        next_generic_obj = object_list[next_id]
        next_scope = next_generic_obj.scope
        next_obj = procedural_objects.Procedural_object(next_id, start_pos, next_scope, next_id)
        next_choice = cur_generic_obj.execute_rule(next_id)
        cur_obj = production_list[tempt_count]
        next_obj.set_position(cur_obj, next_choice)

        cur_obj = next_obj
        production_list.append(cur_obj)
    
        count += 1

    return production_list