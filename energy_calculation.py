#1.BVT

from math import floor

NUMOFSLOTS=2000


def slotsEnergyBVT(slots,dist_arr):
    tot_energy=0
    for i,slot in enumerate(slots):
        dist=dist_arr[i]

        sm=0
        if(2000<dist<=4000):
            #BPSK
            sm=12.5
        elif 1000<dist<=2000 :
            #QPSK
            sm=25
        elif 500<dist<=1000 :
            #8QAM
            sm=37.5
        elif 0<dist<=500:
            sm=50
        
        
        em=1.683*sm+91.333
        path_energy=slot*em
        tot_energy+=path_energy
    return tot_energy


def amplifier_energy(slots_list,paths,adj_matrix):
    tot_energy=0
    for idx,tot_path in enumerate(paths):
        each_path_energy=0
        slots=slots_list[idx]
        tuple_list = [(tot_path[i], tot_path[i+1]) if tot_path[i] < tot_path[i+1] else (tot_path[i+1], tot_path[i]) for i in range(len(tot_path)-1)]
        
        for link in tuple_list:
            link_length=adj_matrix[link[0]-1][link[1]-1]
            amp_energy=floor(link_length/80 + 1)*100
            each_path_energy+=amp_energy
        
        tot_pow_given_slot=slots/NUMOFSLOTS*each_path_energy
        tot_energy+=tot_pow_given_slot
    return tot_energy

def crossConnect_energy(slots_list,paths,node_degree):
    
    tot_energy=0
    for idx,each_path in enumerate(paths):
        slots=slots_list[idx]
        each_node=each_path[:-1]
        for node in each_node:
            ev=85*(node_degree[node-1]-1)+100*20+150 #add_drop degree D=20
            tot_energy+=slots/NUMOFSLOTS*ev
    return tot_energy
