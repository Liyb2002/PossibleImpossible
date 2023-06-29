import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate

import numpy as np

#read the inputs
generic_object_list = []
with open('objects.json', 'r') as object_file:
    objects_data = json.load(object_file)

    generic_object_list.append(generic_objects.Generic_object(objects_data[0]))
    for object_data in objects_data:
        new_object = generic_objects.Generic_object(object_data)
        generic_object_list.append(new_object)



startPos = np.array([400,400])
class_generate = generate.generate_helper(generic_object_list)
result_list = class_generate.smc_process(startPos)


# phase1, phase2, phase3 = class_generate.recursive_process()

print("success!")




output_writer = write2JSON.output()

output_writer.write_proceudral_objects(class_generate.small_cubes, './three/guides.json')
output_writer.write_proceudral_objects(result_list, './three/result.json')

# output_writer.write_result(result_list, './three/result.json')
