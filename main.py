import json
import write2JSON
import intersection
import produce
import generic_objects
import cycle_connect
import particle
import decorations
import assign_type
import parseTree

import numpy as np

#find impossible intersection positions
startPos = np.array([400,400])
basic_scene = intersection.Scene(startPos)
foreground_index = 8
background_index = 16

foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
background_intersection = basic_scene.get_possible_intersects(background_index)

#read the inputs
generic_object_list = []
with open('objects.json', 'r') as object_file:
    objects_data = json.load(object_file)

    generic_object_list.append(generic_objects.Generic_object(objects_data[0]))
    for object_data in objects_data:
        new_object = generic_objects.Generic_object(object_data)
        generic_object_list.append(new_object)

#parse probability tree
parsedProb = parseTree.parseProb(generic_object_list, generic_object_list[1])
#start produce
foreground_type = 1
foreground_connect = "-y"
background_type = 3
background_connect = "+y"

steps = 2

success = False
while(success != True):
    print("-----------------")
    cur_particle = particle.Particle(generic_object_list)
    ok = cur_particle.run_particle(foreground_intersection, foreground_type, foreground_connect, steps, True)
    if not ok :
        continue
    ok = cur_particle.run_particle(background_intersection, background_type, background_connect, steps, False)
    if not ok :
        continue

    cur_particle.run_connect()
    # cur_particle.run_particle2(steps+2)

    cur_particle.overlapping_check()
    success = cur_particle.success

procedural_objects = assign_type.assign(cur_particle.procedural_objects)

decorator = decorations.decoration_operator()
decoration_list = decorator.decorate(cur_particle.procedural_objects)


output_writer = write2JSON.output()
# output_writer.prepare_write_debug(cur_particle.procedural_objects)
output_writer.prepare_write_decorations(decoration_list)
output_writer.write()

