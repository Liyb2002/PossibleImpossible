import json
import generic_objects
import procedural_objects

import numpy as np

object_list = []
production_list = []
if __name__ == "__main__":
    with open('objects.json', 'r') as object_file:
        objects_data = json.load(object_file)

        object_list.append(objects_data[0])
        for object_data in objects_data:
            new_object = generic_objects.Generic_object(object_data)
            object_list.append(new_object)

cur_id = 1
cur_pos = np.array([0,0,0])
cur_scope = object_list[cur_id].scope
cur_obj = procedural_objects.Procedural_object(cur_id)
cur_obj.set_position(cur_pos)
cur_obj.set_scope(cur_scope)
cur_generic_obj = object_list[cur_id]
next_id = cur_generic_obj.get_next()
cur_generic_obj.execute_rule(next_id)

#processing
# count = 0
# while(True):
#     cur_obj = procedural_objects.Procedural_object(cur_id)
#     cur_obj.set_position(cur_pos)
#     cur_obj.set_scope(cur_scope)
#     production_list.append(cur_obj)

#     cur_generic_obj = object_list[cur_id]
#     next_id = cur_generic_obj.get_next()
#     if next_id == None:
#         break

    

#show the objects we have
# for obj in production_list:
#     print("object type",obj.type, "position", obj.position, "scope", obj.scope)