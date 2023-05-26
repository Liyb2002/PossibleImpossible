import produce
import cycle_connect
import random
import procedural_objects
import numpy as np

class Particle:
    def __init__(self, generic_object_list):
        self.generic_object_list = generic_object_list
        self.success = True
        self.procedural_objects = []
        self.targetProb = {}


    def run_particle(self,intersection, start_type, connected_dir, steps, targetProb, isFront):
        cur_obj = start_obj(intersection, self.generic_object_list, start_type, connected_dir)
        self.procedural_objects.append(cur_obj)
        self.targetProb = targetProb

        if isFront:
            step = 0
            while step < steps:
                step +=1
                results = produce.execute_model(self.generic_object_list, cur_obj, 1)
                if len(results) == 0:
                    return False
                cur_obj = results[-1]
                self.procedural_objects += results
                self.density_score()
                self.probability_score()

            self.start_connect = self.procedural_objects[-1]
            return True

        else:
            step = 0
            while step < steps:
                step +=1
                results = produce.execute_model(self.generic_object_list, cur_obj, steps)
                if len(results) == 0:
                    return False
                cur_obj = results[-1]
                self.procedural_objects += results

            self.end_connect = self.procedural_objects[-1]
            return True

    def run_connect(self):
        connect_list = cycle_connect.solve_3D(self.generic_object_list, self.start_connect, self.end_connect)
        if len(connect_list) == 0:
            print("failed connect")
            self.success = False
        else:
            print("success connect")
        self.procedural_objects += connect_list
    
    def run_particle2(self, steps):
        rd1, rd2 = self.random_object()
        objStart = self.procedural_objects[rd1]
        objStart2 = self.procedural_objects[rd2]

        self.procedural_objects += produce.execute_model(self.generic_object_list, objStart, steps)
        self.start_connect = self.procedural_objects[-1]
        self.procedural_objects += produce.execute_model(self.generic_object_list, objStart2, steps)
        self.end_connect = self.procedural_objects[-1]

    def overlapping_check(self):
        for obj_A in self.procedural_objects:
            for obj_B in self.procedural_objects:
                if obj_A.hash != obj_B.hash:
                    overlapping = obj_A.collision_check(obj_B)
                    if overlapping:
                        self.success = False
            
    def find_connect_ending(self):
        for obj in self.back_list:
            if obj.type == 1:
                return obj
    
    def random_object(self):
        rd1 = 0
        rd2 = 0

        while True:
            rd1 = random.randint(0, len(self.procedural_objects)-1)
            obj1 = self.procedural_objects[rd1]
            #need to work on rules
            if obj1.type == 1:
                break
        
        while True:
            rd2 = random.randint(0, len(self.procedural_objects)-1)
            obj2 = self.procedural_objects[rd2]
            #need to work on rules
            if obj2.type == 1 and rd1 != rd2:
                break

        return (rd1, rd2)
    
    def density_score(self):
        added_object = self.procedural_objects[-1]
        k = 1.0
        expanded_cube_length = added_object.length + np.array([k,k,k])
        expanded_cube_size = expanded_cube_length[0] * expanded_cube_length[1] * expanded_cube_length[2] * 8
        sum_overlapping_size = added_object.length[0] * added_object.length[1] * added_object.length[2] * 8

        for obj in self.procedural_objects[:-1]:
            sum_overlapping_size += procedural_objects.getOverlap3D(added_object.position, expanded_cube_length, obj.position, obj.length)
        
        proportion_score = sum_overlapping_size / expanded_cube_size
        return proportion_score

    def probability_score(self):
        current_Prob = {}
        probability_score = 0

        for generic_obj in self.generic_object_list:
            current_Prob[generic_obj.id] = 0

        for obj in self.procedural_objects:
            current_Prob[obj.type] += 1 / len(self.procedural_objects)
        
        for key in current_Prob:
            diff = current_Prob[key] - self.targetProb[key]
            probability_score += (1-diff) * (1-diff)
        
        return probability_score


def start_obj(start_pos, generic_object_list, start_type, connected_dir):

    cur_type = start_type
    start_scope = generic_object_list[cur_type].scope
    gen_hash = generic_object_list[cur_type].generate_hash()
    cur_obj = procedural_objects.Procedural_object(cur_type, start_pos, start_scope, gen_hash)
    cur_obj_x = cur_obj.length[0]
    cur_obj_y = cur_obj.length[1]
    cur_obj_z = cur_obj.length[2]
    update_pos = np.array([cur_obj_x, cur_obj_y, cur_obj_z])
    cur_obj.arbitrary_set_position(start_pos - update_pos)
    cur_obj.add_connected(connected_dir)

    return cur_obj
