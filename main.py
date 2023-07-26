import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate
import innerLayer
import read_file

import sys
import numpy as np

if len(sys.argv) < 4:
    print("Usage: python main.py <file_path> <decorate_path> <export_path> <optional:matryoshka_path>")
    sys.exit(1)

file_path = sys.argv[1]
decorate_path = sys.argv[2]
export_path = sys.argv[3]
matryoshka_path = file_path

if len(sys.argv) == 5:
    matryoshka_path = sys.argv[4]


#read the inputs
generic_object_list = []
global__object_list = []
extra_system_list = []

visual_bridge_info,generic_object_list,global__object_list,extra_system_list = read_file.read_object_file(file_path)

class_generate = generate.generate_helper(generic_object_list, global__object_list, extra_system_list, visual_bridge_info, decorate_path)
result_list = class_generate.smc_process()


# phase1, phase2, phase3 = class_generate.recursive_process()

print("success!")

result_list += innerLayer.produce_innerLayer(matryoshka_path, decorate_path)



output_writer = write2JSON.output()

# output_writer.write_proceudral_objects(class_generate.small_cubes, './three/guides.json')
# output_writer.write_proceudral_objects(result_list, './three/result.json')

output_writer.write_result(result_list, export_path)
