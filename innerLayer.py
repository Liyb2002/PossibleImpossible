import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate

from copy import deepcopy
import sys
import numpy as np

def produce_innerLayer(generic_object_list, global__object_list, extra_system_list, visual_bridge_info, decorate_path):

    new_generic_object_list = deepcopy(generic_object_list)
    multipler = 0.1

    for new_generic_object in new_generic_object_list:
        new_generic_object.adjust_scope(multipler)


    with open( "inner_layer.json", 'r') as object_file:
        objects_data = json.load(object_file)

        for object_data in objects_data:
            center_x = object_data['obj']['start_x']
            center_y = object_data['obj']['start_y']
            center_z = object_data['obj']['start_z']

            scope_x = object_data['obj']['scale_x']
            scope_y = object_data['obj']['scale_y']
            scope_z = object_data['obj']['scale_z']
            
            
            
            class_generate = generate.generate_helper(generic_object_list, global__object_list, extra_system_list, visual_bridge_info, decorate_path)
            result_list = class_generate.smc_process()
