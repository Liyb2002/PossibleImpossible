from copy import deepcopy

def resample_particles(particle_list, score_list):
    new_particle_list = []

    score_list.sort(key = lambda x : -x[1])

    for pair in score_list:
        if pair[1] > 0:
            new_particle_list.append(particle_list[pair[0]])    

    return new_particle_list
