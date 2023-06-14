
import parseTree
import particle
import intersection
import resample
import assign_type
import decorations
import constraints_loader

import numpy as np

class generate_helper:
    def __init__(self, generic_object_list):
        #find impossible intersection positions

        self.generic_object_list = generic_object_list
        self.particle_list = []
        self.score_list = []
        self.result_particle = None

        self.guided_pts = constraints_loader.load_constraints()
        
    
    def smc_process(self):
        num_particles = 3000
        for i in range(num_particles):
            tempt_particle = particle.Particle(self.generic_object_list, self.guided_pts)
            self.particle_list.append(tempt_particle)

        startPos = np.array([400,400])
        basic_scene = intersection.Scene(startPos)
        foreground_index = 8
        background_index = 16

        foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
        background_intersection = basic_scene.get_possible_intersects(background_index)

        self.small_cubes = constraints_loader.guide_visualizer(self.guided_pts, foreground_index)

        foreground_type = 1
        foreground_connect = "-y"
        background_type = 3
        background_connect = "+y"
        steps = 2

        self.procedural_generate(foreground_type, foreground_connect, foreground_intersection, steps, True)
        self.procedural_generate(background_type, background_connect, background_intersection, steps, False)
        # self.connect()

        self.result_particle = self.particle_list[0]

        for partt in self.particle_list:
            print("hit hit", partt.hit_constraints)
        return self.result_particle.procedural_objects


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
                score_list.append([i, tempt_particle.get_score()])

            self.particle_list = resample.resample_particles(self.particle_list, score_list)

        print("generation complete")



    def connect(self):
        print("len(particle_list)", len(self.particle_list))
        working_list = []
        for i in range(len(self.particle_list)):
            self.particle_list[i].run_connect()
            if self.particle_list[i].success:
                print("success")
                working_list.append(self.particle_list[i])
                
        self.result_particle = self.particle_list[i]


    def finish(self):
        procedural_objects = assign_type.assign(self.result_particle.procedural_objects)
        decorator = decorations.decoration_operator()
        decoration_list = decorator.decorate(self.result_particle.procedural_objects)
        return decoration_list

    def recursive_process(self):
        #phrase: 1->random walk, 2->connect, 3-> decorations
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
        foreground_parsedProb = parseTree.parseProb(self.generic_object_list, self.generic_object_list[foreground_type])

        background_type = 3
        background_connect = "+y"
        background_parsedProb = parseTree.parseProb(self.generic_object_list, self.generic_object_list[background_type])

        steps = 2
        success = False

        phase1 = []
        phase2 = []
        phase3 = []

        decorator = decorations.decoration_operator()
        while(success != True):
            print("-----------------")
            cur_particle = particle.Particle(self.generic_object_list, self.guided_pts)
            cur_particle.prepare_particle(foreground_intersection, foreground_type, foreground_connect, foreground_parsedProb)

            for s in range(steps):
                cur_step = steps - s -1
                cur_particle.run_step(cur_step, True)
            if cur_particle.score == 0:
                continue

            cur_particle.prepare_particle(background_intersection, background_type, background_connect, background_parsedProb)
            for s in range(steps):
                cur_step = steps - s -1
                print("cur_step", cur_step)

                cur_particle.run_step(cur_step, False)
            if cur_particle.score == 0:
                continue

            phase1 = cur_particle.procedural_objects

            cur_particle.run_connect()
            cur_particle.overlapping_check()
            success = cur_particle.success
            if cur_particle.score == 0:
                continue

            phase2 = cur_particle.procedural_objects

        # procedural_objects = assign_type.assign(cur_particle.procedural_objects)

        decoration_list = decorator.decorate(cur_particle.procedural_objects)

        phase3 = decoration_list
        return (phase1, phase2, phase3)
