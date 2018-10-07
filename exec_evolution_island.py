import archipelado as acp 

tempo_ind = 0 
best_gen_each_island = []

def set_best_gen_from_island(best_gen):
    best_gen_each_island[tempo_ind] = best_gen
    tempo_ind + 1   

def get_best_gen_from_island(ind_island):
    return best_gen_each_island[ind_island]

def islands_evolution():    
    tempo_island = []
    for i in range(acp.get_acp_num_threads()):
        tempo_island = acp.get_acp_island(i)
        #send to the evolution process
        acp.set_acp_island(i,tempo_island)
    
        
        