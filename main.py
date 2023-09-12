import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate
import innerLayer
import read_file
import initLSystem

import sys
import numpy as np

if len(sys.argv) < 4:
    print("Usage: python main.py <file_path> <decorate_path> <export_path> <optional:matryoshka_path>")
    sys.exit(1)

file_path = sys.argv[1]
decorate_path = sys.argv[2]
export_path = sys.argv[3]


#read the inputs
generic_object_list = []
global__object_list = []
extra_system_list = []
result_list = []

visual_bridge_info,generic_object_list,global__object_list,extra_system_list = read_file.read_object_file(file_path)
if visual_bridge_info is None:
    result_list = initLSystem.initSystem(decorate_path)
else:
    class_generate = generate.generate_helper(generic_object_list, global__object_list, extra_system_list, visual_bridge_info, decorate_path)
    result_list = class_generate.smc_process()

    print("impossible structure success!")
    if len(sys.argv) == 5:
        matryoshka_path = sys.argv[4]
        result_list += innerLayer.produce_innerLayer(matryoshka_path, decorate_path)



print("success!")
output_writer = write2JSON.output()

# output_writer.write_proceudral_objects(class_generate.small_cubes, './three/guides.json')
# output_writer.write_proceudral_objects(result_list, './three/result.json')

output_writer.write_result(result_list, export_path)
