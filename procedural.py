import json
import generic_objects
import procedural_objects
import write2JSON
import intersection

import numpy as np

startPos = np.array([400,400])
basic_scene = intersection.Scene(startPos)
foreground_index = 8
background_index = 12

foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
background_intersection = basic_scene.get_possible_intersects(background_index)
print("foreground_intersection", foreground_intersection)
print("background_intersection", background_intersection)

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
start_pos = np.array([0,0,0])
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
    next_obj = procedural_objects.Procedural_object(next_id, start_pos, start_scope)
    choice = cur_generic_obj.execute_rule(next_id)
    next_obj.set_position(cur_obj, choice)

    cur_id = next_id
    cur_obj = next_obj
    production_list.append(cur_obj)


write2JSON.write(production_list)
