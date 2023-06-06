
import parseTree
import particle
import intersection
import resample
import assign_type
import decorations

import numpy as np

class generate_helper:
    def __init__(self, generic_object_list):
        #find impossible intersection positions
        startPos = np.array([400,400])
        basic_scene = intersection.Scene(startPos)
        foreground_index = 8
        background_index = 16

        foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
        background_intersection = basic_scene.get_possible_intersects(background_index)

        #parse probability tree
        #start produce
        foreground_type = 1
        foreground_connect = "-y"
        foreground_parsedProb = parseTree.parseProb(generic_object_list, generic_object_list[foreground_type])

        background_type = 3
        background_connect = "+y"
        background_parsedProb = parseTree.parseProb(generic_object_list, generic_object_list[background_type])

        steps = 3

        particle_list = []
        score_list = []
        num_particles = steps * 100


        for i in range(num_particles):
            tempt_particle = particle.Particle(generic_object_list)
            tempt_particle.prepare_particle(foreground_intersection, foreground_type, foreground_connect, foreground_parsedProb)
            particle_list.append(tempt_particle)

        for s in range(steps):
            cur_step = steps - s -1
            print("cur_step", cur_step)

            score_list = []
            for i in range(len(particle_list)):
                tempt_particle = particle_list[i]
                tempt_particle.run_step(cur_step, True)
                score_list.append(tempt_particle.get_score())

            particle_list = resample.resample_particles(particle_list, score_list)

        print("front generation complete")

        for i in range(len(particle_list)):
            tempt_particle = particle_list[i]
            tempt_particle.prepare_particle(background_intersection, background_type, background_connect, background_parsedProb)
            
        for s in range(steps):
            cur_step = steps - s -1

            score_list = []
            for i in range(len(particle_list)):
                tempt_particle = particle_list[i]
                tempt_particle.run_step(cur_step, False)
                score_list.append(tempt_particle.get_score())

            particle_list = resample.resample_particles(particle_list, score_list)

        print("back generation complete")


        result_particle = None
        print("len(particle_list)", len(particle_list))
        for i in range(len(particle_list)):
            particle_list[i].run_connect()
            if particle_list[i].success:
                print("success")
                result_particle = particle_list[i]
                break



        procedural_objects = assign_type.assign(result_particle.procedural_objects)
        decorator = decorations.decoration_operator()
        self.decoration_list = decorator.decorate(result_particle.procedural_objects)
