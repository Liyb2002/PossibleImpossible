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
        self.eye=np.array([5.0, 5.0, 5.0])


    def run_particle(self,intersection, start_type, connected_dir, steps, targetProb, isFront):
        cur_obj = start_obj(intersection, self.generic_object_list, start_type, connected_dir)
        intersection_obj = cur_obj
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
                self.occulusion_score(intersection_obj, results)

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
        startPos = self.start_connect.position
        endPos = self.end_connect.position

        delta = endPos - startPos

        production_list = []
        production_list.append(self.start_connect)
        abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
        abs_delta -= np.array([0, 0, self.end_connect.length[2]])

        directions = cycle_connect.get_dirs(delta)
        directions = cycle_connect.update_order(self.start_connect, directions)
        orders = cycle_connect.random_order()

        for i in range(0,3):
            index = orders[i]
            if abs_delta[index] != 0:
                available_endings = cycle_connect.Available_Ending_With_Direction(self.generic_object_list, directions[index])

                if i == 2:
                    available_endings = cycle_connect.Available_Ending_With_Object(self.generic_object_list, self.end_connect)

                connect_particle = produce.connect_execution(production_list[-1], self.generic_object_list,abs_delta,directions[index],available_endings, self.end_connect)
                ok = 1

                while ok == 1:
                    ok = connect_particle.execute_model_withDirection()
                
                if ok == 0:
                    self.success = False
                    return 
                
                if ok == 2:
                    production_list += connect_particle.set_scope()




        # for i in range(0,3):
        #     ok, tempt_result = cycle_connect.single_execution(abs_delta, orders[i], self.generic_object_list, directions, production_list, self.end_connect, i)
        #     if not ok:
        #         self.success = False
        #         return 
        #     production_list += tempt_result

        self.procedural_objects += production_list
    
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

    def occulusion_score(self, intersection_obj, new_Obj_list):
        occulusion_score = 0
        for obj in new_Obj_list:
            occulusion_score += 200
            occulusion_score += check_occlusion(obj, intersection_obj, self.eye)




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

def check_occlusion(front_obj, back_obj, eye):
    score = 0

    pt0 = back_obj.position
    ray0 = pt0 - eye
    ray0 = ray0 / np.linalg.norm(ray0)
    is_occluded =  ray_intersecting_Obj(front_obj, ray0, eye)
    if is_occluded:
        score -= 100

    pt1 = back_obj.position + back_obj.length
    ray1 = pt1 - eye
    ray1 = ray1 / np.linalg.norm(ray1)
    is_occluded =  ray_intersecting_Obj(front_obj, ray1, eye)
    if is_occluded:
        score -= 50


    pt2 = back_obj.position - back_obj.length
    ray2 = pt2 - eye
    ray2 = ray2 / np.linalg.norm(ray2)
    is_occluded =  ray_intersecting_Obj(front_obj, ray2, eye)
    if is_occluded:
        score -= 50
    
    return score



def ray_intersecting_Obj(front_obj, ro, rd):
    minX = front_obj.position[0] - front_obj.length[0]
    maxX = front_obj.position[0] + front_obj.length[0]
    minY = front_obj.position[1] - front_obj.length[1]
    maxY = front_obj.position[1] + front_obj.length[1]
    minZ = front_obj.position[2] - front_obj.length[2]
    maxZ = front_obj.position[2] + front_obj.length[2]

    tMin = (minX - ro[0]) / rd[0]
    tMax = (maxX - ro[0]) / rd[0]

    if tMin > tMax:
        swap(tMin, tMax)
    
    tMinY = (minY - ro[1]) / rd[1]
    tMaxY = (maxY - ro[1]) / rd[1]
    if tMinY > tMaxY:
        swap(tMinY, tMaxY)

    if (tMin > tMaxY) or (tMinY > tMax):
        return False
    
    if tMinY > tMin:
        tMin = tMinY

    if tMaxY < tMax:
        tMax = tMaxY
    
    tMinZ = (minZ - ro[2]) / rd[2]
    tMaxZ = (maxZ - ro[2]) / rd[2]

    if tMinZ > tMaxZ:
        swap(tMinZ, tMaxZ)
    
    if (tMin > tMaxZ) or (tMinZ > tMax):
        return False
    
    return True

