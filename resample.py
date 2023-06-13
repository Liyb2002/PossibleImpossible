from copy import deepcopy

def resample_particles(particle_list, score_list):
    new_particle_list = []

    print(score_list)

    for particle in particle_list:
        if particle.get_score() > 0:
            new_particle_list.append(particle)
    

    return new_particle_list
