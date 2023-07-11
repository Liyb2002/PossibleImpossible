
import parseTree
import particle
import intersection
import resample
import assign_type
import decorations
import perspective
import constraints_loader
import global_execution

from copy import deepcopy
import numpy as np

class generate_helper:
    def __init__(self, generic_object_list, global__object_list, visual_bridge_info, decorate_path):
        #find impossible intersection positions

        self.generic_object_list = generic_object_list
        self.global__object_list = global__object_list
        self.particle_list = []
        self.score_list = []
        self.result_particle = None
        self.sampled_points = constraints_loader.load_constraints()
        self.visual_bridge_info = visual_bridge_info
        self.decorate_path = decorate_path
    
    def smc_process(self):
        num_particles = 3000
        for i in range(num_particles):
            tempt_particle = particle.Particle(self.generic_object_list, self.sampled_points)
            self.particle_list.append(tempt_particle)

        startPos = np.array([400,400])
        foreground_index = 12
        background_index = 24

        camera = perspective.ortho_camera()
        foreground_intersection, background_intersection = camera.get_intersections(startPos, foreground_index, background_index)


        foreground_type = self.visual_bridge_info['foreground_type'][0]
        foreground_connect = self.visual_bridge_info['foreground_connect']
        background_type = self.visual_bridge_info['background_type']
        background_connect = self.visual_bridge_info['background_connect']

        steps = 2

        self.small_cubes = constraints_loader.guide_visualizer(self.sampled_points, foreground_index)

        self.procedural_generate(foreground_type, foreground_connect, foreground_intersection, steps, True)
        if background_type != 0:
            self.procedural_generate(background_type, background_connect, background_intersection, steps, False)
        
        tempt_list = []
        for temple_particle in self.particle_list:
            if temple_particle.success:
                tempt_list.append(temple_particle)
        self.particle_list = tempt_list
        print("len(tempt_list)", len(tempt_list))
        self.connect()


        # self.reproduce_particle_list(num_particles)
        # startPos = np.array([100,800])
        # foreground_intersection, background_intersection = camera.get_intersections(startPos, foreground_index, background_index)
        # self.procedural_generate(foreground_type, foreground_connect, foreground_intersection+np.array([0.05,0.075,0.05]), steps, True)
        # self.procedural_generate(background_type, background_connect, background_intersection-np.array([0.05,0.15,0.05]), steps, False)
        # self.connect()

        self.select_result_particle()
        return self.finish()
        # return self.particle_list[0].procedural_objects


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
        print("to connect, len(particle_list)", len(self.particle_list))

        success_connect_list = []
        for i in range(len(self.particle_list)):
            self.particle_list[i].run_connect()
            if self.particle_list[i].success:
                success_connect_list.append(self.particle_list[i])

        self.particle_list = success_connect_list
        print("successful connected particle list", len(self.particle_list))

    def select_result_particle(self):
        highest_hit = 0
        self.result_particle = self.particle_list[0]
        for particle in self.particle_list:
            if particle.hit_constraints > highest_hit:
                self.result_particle = particle
                highest_hit = particle.hit_constraints

    def reproduce_particle_list(self, num_particles):
        new_particle_list = []
        multipler = int(num_particles / len(self.particle_list)) + 1

        for particle in self.particle_list:
            for i in range(0, multipler):
                copied_particle = deepcopy(particle)
                new_particle_list.append(copied_particle)

        self.particle_list = new_particle_list


    def finish(self):
        self.result_particle.procedural_objects[0].type = self.visual_bridge_info['foreground_type'][1]
        procedural_objects = global_execution.global_assign(self.result_particle.procedural_objects, self.global__object_list)
        decorator = decorations.decoration_operator(self.decorate_path)
        decoration_list = decorator.decorate(procedural_objects)
        return decoration_list

    def recursive_process(self):
        #phrase: 1->random walk, 2->connect, 3-> decorations
        #find impossible intersection positions
        startPos = np.array([400,400])
        foreground_index = 8
        background_index = 16

        camera = perspective.ortho_camera()
        foreground_intersection, background_intersection = camera.get_intersections(startPos, foreground_index, background_index)

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
