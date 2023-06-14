import json
import random
import numpy as np
import procedural_objects
import intersection

def load_constraints():
    sampled_points = []
    with open('guide.json', 'r') as object_file:
        guides = json.load(object_file)

        for guide_obj in guides:
            startPos = guide_obj['startPos']
            endPos = guide_obj['endPos']
            
            for i in range(20):
                random_x = random.randint(startPos[0], endPos[0])
                random_y = random.randint(startPos[1], endPos[1])
                newPt = [random_x, random_y]
                sampled_points.append(newPt)        
    
    return sampled_points

def guide_visualizer(sampled_points, foreground_index):
    dummy_Pos = np.array([0,0])
    dummy_scope = [0.02, 0.02]
    basic_scene = intersection.Scene(dummy_Pos)

    small_cubes = []
    for pts in sampled_points:
        pos = basic_scene.get_arbitrary_pos(foreground_index, pts)
        cube = procedural_objects.Procedural_object(-1, pos, np.array([dummy_scope,dummy_scope,dummy_scope]), "00000")
        small_cubes.append(cube)
    
    return small_cubes
