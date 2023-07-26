import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate
import innerLayer

import sys
import numpy as np

#read the inputs
generic_object_list = []
global__object_list = []
extra_system_list = []

visual_bridge_info = None

if len(sys.argv) < 4:
    print("Usage: python main.py <file_path> <decorate_path> <export_path>")
    sys.exit(1)

file_path = sys.argv[1]
decorate_path = sys.argv[2]
export_path = sys.argv[3]

with open( file_path, 'r') as object_file:
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
            if object_data['type'] == "extra_system":
                extra_system_list.append(object_data)
                new_object = generic_objects.Generic_object(object_data)
                generic_object_list.append(new_object)



class_generate = generate.generate_helper(generic_object_list, global__object_list, extra_system_list, visual_bridge_info, decorate_path)
result_list = class_generate.smc_process()


# phase1, phase2, phase3 = class_generate.recursive_process()

print("success!")

innerLayer.produce_innerLayer()



output_writer = write2JSON.output()

# output_writer.write_proceudral_objects(class_generate.small_cubes, './three/guides.json')
# output_writer.write_proceudral_objects(result_list, './three/result.json')

output_writer.write_result(result_list, export_path)
