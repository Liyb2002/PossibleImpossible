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


class_generate = generate.generate_helper(generic_object_list)
decoration_list = class_generate.smc_process()


phase1, phase2, phase3 = class_generate.recursive_process()

print("success!")




output_writer = write2JSON.output()
# output_writer.prepare_write_debug(cur_particle.procedural_objects)
# output_writer.prepare_write_skeleton(phase1)
# output_writer.write_phase1()

output_writer.write_skeleton(phase2, './three/phase2.json')
output_writer.write_result(phase3, './three/phase3.json')

# output_writer.write_small_cubes(class_generate.small_cubes)

# output_writer.prepare_write_decorations(decoration_list)
# output_writer.write()

