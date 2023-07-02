import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate

import numpy as np

#read the inputs
generic_object_list = []
global__object_list = []
visual_bridge_info = None

with open('tree/tree.json', 'r') as object_file:
    objects_data = json.load(object_file)

    generic_object_list.append(generic_objects.Generic_object(objects_data[1]))
    for object_data in objects_data:
        if object_data['object_id'] == -1:
            visual_bridge_info = object_data
        if object_data['object_id'] > 0:
            if object_data['type'] == "local_object":
                new_object = generic_objects.Generic_object(object_data)
                generic_object_list.append(new_object)
            if object_data['type'] == "global_object":
                global__object_list.append(object_data)


class_generate = generate.generate_helper(generic_object_list, global__object_list, visual_bridge_info)
result_list = class_generate.smc_process()


# phase1, phase2, phase3 = class_generate.recursive_process()

print("success!")




output_writer = write2JSON.output()

output_writer.write_proceudral_objects(class_generate.small_cubes, './three/guides.json')
# output_writer.write_proceudral_objects(result_list, './three/result.json')

output_writer.write_result(result_list, './three/result.json')
