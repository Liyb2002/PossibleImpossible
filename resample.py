from copy import deepcopy


def resample_particles(particle_list, score_list):
    num_particles = len(particle_list)
    num_favorable = int(num_particles / 10)
    new_particle_list = []

    for particle in particle_list:
        if particle.get_score() > 0:
            new_particle_list.append(particle)
    
    return new_particle_list

    # sorted_index = sorted(range(len(score_list)), key=lambda k: score_list[k])
    # sorted_index.reverse()

    # considered_total = 0

    # for i in range(num_favorable):
    #     best_index = sorted_index[i]
    #     considered_total += score_list[best_index]

    # for i in range(num_favorable):
    #     best_index = sorted_index[i]
    #     cur_score = score_list[best_index]
    #     num_copies = int(cur_score/considered_total * num_particles)

    #     for j in range(num_copies):
    #         cur_particle = deepcopy(particle_list[best_index])
    #         new_particle_list.append(cur_particle)
    
    # for i in range(num_particles - len(new_particle_list)):
    #     best_index = sorted_index[0]
    #     cur_particle = deepcopy(particle_list[best_index])
    #     new_particle_list.append(cur_particle)

    # return new_particle_list