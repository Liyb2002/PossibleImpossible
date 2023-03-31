import json
import generic_objects
import procedural_objects

object_list = []
production_list = []
if __name__ == "__main__":
    with open('objects.json', 'r') as object_file:
        objects_data = json.load(object_file)

        object_list.append(objects_data[0])
        for object_data in objects_data:
            new_object = generic_objects.Generic_object(object_data)
            object_list.append(new_object)

cur_id = 2

while(True):
    cur_obj = procedural_objects.Procedural_object(cur_id)
    production_list.append(cur_obj)
    generic_obj = object_list[cur_id]
    cur_id = generic_obj.get_next()

    if cur_id == None:
        break