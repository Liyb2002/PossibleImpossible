
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

        self.generic_object_list = generic_object_list
        self.particle_list = []
        self.score_list = []
        self.result_particle = None

        num_particles = 1000
        for i in range(num_particles):
            tempt_particle = particle.Particle(self.generic_object_list)
            self.particle_list.append(tempt_particle)

        startPos = np.array([400,400])
        basic_scene = intersection.Scene(startPos)
        foreground_index = 8
        background_index = 16

        foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
        background_intersection = basic_scene.get_possible_intersects(background_index)

        foreground_type = 1
        foreground_connect = "-y"
        background_type = 3
        background_connect = "+y"
        steps = 3

        self.procedural_generate(foreground_type, foreground_connect, foreground_intersection, steps, True)
        self.procedural_generate(background_type, background_connect, background_intersection, steps, False)
        self.connect()
        
    
    def procedural_generate(self, start_type, connect_direction, intersection_pos, steps, isFront):
        parsedProb = parseTree.parseProb(self.generic_object_list, self.generic_object_list[start_type])

        score_list = []

        for i in range(len(self.particle_list)):
            tempt_particle = self.particle_list[i]
            tempt_particle.prepare_particle(intersection_pos, start_type, connect_direction, parsedProb)

        for s in range(steps):
            cur_step = steps - s -1
            print("cur_step", cur_step)

            score_list = []
            for i in range(len(self.particle_list)):
                tempt_particle = self.particle_list[i]
                tempt_particle.run_step(cur_step, isFront)
                score_list.append(tempt_particle.get_score())

            self.particle_list = resample.resample_particles(self.particle_list, score_list)

        print("generation complete")



    def connect(self):
        print("len(particle_list)", len(self.particle_list))
        for i in range(len(self.particle_list)):
            self.particle_list[i].run_connect()
            if self.particle_list[i].success:
                print("success")
                self.result_particle = self.particle_list[i]
                break


    def finish(self):
        procedural_objects = assign_type.assign(self.result_particle.procedural_objects)
        decorator = decorations.decoration_operator()
        decoration_list = decorator.decorate(self.result_particle.procedural_objects)

        return decoration_list
