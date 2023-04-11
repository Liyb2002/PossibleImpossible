import json
import write2JSON
import intersection
import produce
import generic_objects

import numpy as np

#find impossible intersection positions
startPos = np.array([400,400])
basic_scene = intersection.Scene(startPos)
foreground_index = 8
background_index = 12

foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
background_intersection = basic_scene.get_possible_intersects(background_index)

#read the inputs
object_list = []
with open('objects.json', 'r') as object_file:
    objects_data = json.load(object_file)

    object_list.append(objects_data[0])
    for object_data in objects_data:
        new_object = generic_objects.Generic_object(object_data)
        object_list.append(new_object)

#start produce
production_list = produce.execute_model(foreground_intersection, object_list, 3, 5)
production_list += produce.execute_model(background_intersection, object_list, 5, 5)


write2JSON.write(production_list)
