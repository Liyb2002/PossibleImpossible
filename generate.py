
import parseTree
import particle
import resample
import assign_type
import decorations
import constraints_loader
import perspective

from copy import deepcopy

import numpy as np

class generate_helper:
    def __init__(self, generic_object_list):
        #find impossible intersection positions

        self.generic_object_list = generic_object_list
        self.particle_list = []
        self.score_list = []
        self.result_particle = None
        self.sampled_points = constraints_loader.load_constraints()
        
    
    def smc_process(self, startPos):
        num_particles = 3000
        for i in range(num_particles):
            tempt_particle = particle.Particle(self.generic_object_list, self.sampled_points)
            self.particle_list.append(tempt_particle)

        foreground_index = 8
        background_index = 16


        camera = perspective.ortho_camera()
        foreground_intersection, background_intersection = camera.get_intersections(startPos, foreground_index, background_index)

        foreground_type = 1
        foreground_connect = "-y"
        background_type = 3
        background_connect = "+y"
        steps = 1

        print("foreground_intersection", foreground_intersection, "background_intersection", background_intersection)
        self.small_cubes = constraints_loader.guide_visualizer(self.sampled_points, foreground_index)
        self.procedural_generate(foreground_type, foreground_connect, foreground_intersection, steps, True)
        self.procedural_generate(background_type, background_connect, background_intersection, steps, False)
        self.connect()

        # self.reproduce_particle_list(num_particles)

        # basic_scene2 = intersection.Scene(np.array([100,100]))
        # foreground_index = 8
        # background_index = 16

        # foreground_intersection = basic_scene2.get_possible_intersects(foreground_index)
        # background_intersection = basic_scene2.get_possible_intersects(background_index)

        # foreground_type = 1
        # foreground_connect = "-y"
        # background_type = 3
        # background_connect = "+y"
        # steps = 1

        # self.procedural_generate(foreground_type, foreground_connect, foreground_intersection, steps, True)
        # self.procedural_generate(background_type, background_connect, background_intersection, steps, False)
        # self.connect()

        self.select_result_particle()
        return self.result_particle.procedural_objects
        # return self.particle_list[0].procedural_objects

    def procedural_generate(self, start_type, connect_direction, intersection_pos, steps, isFront):
        parsedProb = parseTree.parseProb(self.generic_object_list, self.generic_object_list[start_type])

        score_list = []

        for i in range(len(self.particle_list)):
            tempt_particle = self.particle_list[i]
            tempt_particle.prepare_particle(intersection_pos, start_type, connect_direction, parsedProb)

        for s in range(steps):
            cur_step = steps - s -1
            # print("cur_step", cur_step)

            score_list = []
            for i in range(len(self.particle_list)):
                tempt_particle = self.particle_list[i]
                tempt_particle.run_step(cur_step, isFront)
                score_list.append(tempt_particle.get_score())

            self.particle_list = resample.resample_particles(self.particle_list, score_list)

        print("random walk phase complete")



    def connect(self):
        print("to connect, len(particle_list)", len(self.particle_list))

        success_connect_list = []
        for i in range(len(self.particle_list)):
            self.particle_list[i].run_connect()
            if self.particle_list[i].success:
                success_connect_list.append(self.particle_list[i])

        self.particle_list = success_connect_list
    
    def select_result_particle(self):
        highest_hit = 0
        for particle in self.particle_list:
            if particle.hit_constraints > highest_hit:
                self.result_particle = particle
                highest_hit = particle.hit_constraints
                print("current hit", particle.hit_constraints)
    
        # print("hit result", self.result_particle.hit_constraints)

    def reproduce_particle_list(self, num_particles):
        new_particle_list = []
        multipler = int(num_particles / len(self.particle_list)) + 1

        for particle in self.particle_list:
            for i in range(0, multipler):
                copied_particle = deepcopy(particle)
                new_particle_list.append(copied_particle)

        self.particle_list = new_particle_list

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
            cur_particle = particle.Particle(self.generic_object_list)
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
