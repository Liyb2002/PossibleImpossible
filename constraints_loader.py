import json
import random
import numpy as np

def load_constraints():
    sampled_points = []
    with open('guide.json', 'r') as object_file:
        guides = json.load(object_file)

        for guide_obj in guides:
            startPos = guide_obj['startPos']
            endPos = guide_obj['endPos']
            
            for i in range(10):
                random_x = random.randint(startPos[0], endPos[0])
                random_y = random.randint(startPos[1], endPos[1])
                newPt = [random_x, random_y]
                sampled_points.append(newPt)
                print("newPt", newPt)
        
    
    return sampled_points