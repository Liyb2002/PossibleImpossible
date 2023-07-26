import json
import write2JSON
import produce
import generic_objects
import cycle_connect
import generate

import sys
import numpy as np

def produce_innerLayer():
    with open( "inner_layer.json", 'r') as object_file:
        objects_data = json.load(object_file)

        for object_data in objects_data:
            center_x = object_data['obj']['start_x']
            center_y = object_data['obj']['start_y']
            center_z = object_data['obj']['start_z']

            scope_x = object_data['obj']['scale_x']
            scope_y = object_data['obj']['scale_y']
            scope_z = object_data['obj']['scale_z']
