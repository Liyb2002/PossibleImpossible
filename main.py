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
import resample

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
#start produce
foreground_type = 1
foreground_connect = "-y"
foreground_parsedProb = parseTree.parseProb(generic_object_list, generic_object_list[foreground_type])

background_type = 3
background_connect = "+y"
background_parsedProb = parseTree.parseProb(generic_object_list, generic_object_list[background_type])

steps = 2

particle_list = []
score_list = []
num_particles = 1000


for i in range(num_particles):
    tempt_particle = particle.Particle(generic_object_list)
    tempt_particle.prepare_particle(foreground_intersection, foreground_type, foreground_connect, foreground_parsedProb)
    particle_list.append(tempt_particle)

for s in range(steps):
    cur_step = steps - s -1

    score_list = []
    print("len(particle_list)", len(particle_list))
    for i in range(len(particle_list)):
        tempt_particle = particle_list[i]
        tempt_particle.run_step(cur_step, True)
        score_list.append(tempt_particle.get_score())

    particle_list = resample.resample_particles(particle_list, score_list)

for i in range(len(particle_list)):
    tempt_particle = particle_list[i]
    tempt_particle.prepare_particle(background_intersection, background_type, background_connect, background_parsedProb)
    
for s in range(steps):
    cur_step = steps - s -1

    for i in range(len(particle_list)):
        tempt_particle = particle_list[i]
        tempt_particle.run_step(cur_step, False)
        score_list.append(tempt_particle.get_score())

    particle_list = resample.resample_particles(particle_list, score_list)



score_list = []
result_particle = None
for i in range(len(particle_list)):
    particle_list[i].run_connect()
    if particle_list[i].success:
        print("success")
        result_particle = particle_list[i]
        break



procedural_objects = assign_type.assign(result_particle.procedural_objects)

decorator = decorations.decoration_operator()
decoration_list = decorator.decorate(result_particle.procedural_objects)

print("success!")

for s in range(steps):
    cur_step = steps - s -1
    print("cur_step", cur_step)

output_writer = write2JSON.output()
# output_writer.prepare_write_debug(cur_particle.procedural_objects)
output_writer.prepare_write_decorations(decoration_list)
output_writer.write()

