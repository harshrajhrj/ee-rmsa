"""find regen nodes from a graph by selecting 20% of highest degree nodes
Block request if the path dist exceds optical reach by returning false"""

from itertools import combinations
from math import ceil
import sys
from findinNoOfSlot import GUARD

OPTICAL_REACH = 4000 


max_int_value = sys.maxsize



def check_optical_reach_blocking_min_freqslot(tree_path_dist, tree_path, regen_node_limit, adj_mat,bw):
    n_tree_path_dist = []
    n_tree_path = []
    regen_happened=[]
    
    for i, dist in enumerate(tree_path_dist):
        path = tree_path[i]
        if dist > OPTICAL_REACH:
            possible_reg_nodes = path[1:-1]        #[5800, 5000, 4000, 1100, 2350]  [21, 16, 17, 18]
            number_of_regen = 1 
            max_regen = len(possible_reg_nodes)  
            while(number_of_regen<=max_regen):
                min_slot_reg_nodes = possible_regenerate(path,adj_mat,number_of_regen,bw,regen_node_limit)
                
                if(min_slot_reg_nodes == True):
                    number_of_regen+=1
                else:
                    distance_list,path_list,regenerated_at = min_slot_reg_nodes
                    for dist_of in distance_list:
                        n_tree_path_dist.append(dist_of)
                    for one_path in path_list:
                        n_tree_path.append(one_path)
                    regen_happened.extend(regenerated_at)
                    for node in regenerated_at:
                        regen_node_limit[node] -= 1
                    break

            
                

            
            if(number_of_regen == max_regen + 1):
                print("!!!!!  CAN'T REGENARATE at any point in path ")
                return True
                


            



        else:
            n_tree_path_dist.append(dist)
            n_tree_path.append(path)
    
    return n_tree_path_dist, n_tree_path, regen_node_limit, regen_happened


def totalFreqSlot(dist,bandwidth):
    mf=0
    if(2000<dist<=4000):
        mf=1
    elif 1000<dist<=2000 :
        mf=2
    elif 500<dist<=1000 :
        mf=3
    elif 0<dist<=500: 
        mf=4
    num_slot=ceil(bandwidth/(12.5*mf))+GUARD
    return num_slot


def possible_regenerate(path,adj_mat,number_of_regen,bandwidth,regen_node_limit):
    possible_reg_nodes = path[1:-1]
    all_combinations = list(combinations(possible_reg_nodes, number_of_regen))#[(1),(2),(3)]..
    least_slot = max_int_value
    distances = []
    paths = []
    regen_possible = False
    combination_used = []

    for each_comb in all_combinations:
        segmented_path = []
        current_sublist = []
        regenerators_end=False
        for i in each_comb:
            if(regen_node_limit[i] == 0):
                regenerators_end=True
                
        if regenerators_end is True:
            continue

        for item in path:
            current_sublist.append(item)

            if item in each_comb:
                segmented_path.append(current_sublist)
                current_sublist = [item]

        if current_sublist:
            segmented_path.append(current_sublist)


        result = find_slots(segmented_path,adj_mat,bandwidth)
        
        if(result == True):
            continue
        num_slots,dist_list = result
        if(num_slots<=least_slot):
            least_slot = num_slots
            distances = dist_list
            paths = segmented_path
            combination_used = list(each_comb)
            regen_possible = True
    if(regen_possible == False):
        return True
    else:
        return distances,paths,combination_used
    
def find_slots(segmented_path,adj_mat,bandwidth): 
    #find the distances of the segments
    distance_segments = []
    freq_slots = 0
    each_path_links=[]
    for each_path in segmented_path:
        past_dist = 0
        each_path_nodes=len(each_path)-1
        each_path_links.append(each_path_nodes)
        for j in range(len(each_path) - 1):
                seg = past_dist + adj_mat[each_path[j] - 1][each_path[j + 1] - 1]
                past_dist = seg
        distance_segments.append(seg)
    for idx,each_dist in enumerate(distance_segments):
        if(each_dist>OPTICAL_REACH):
            return True
        
        freq_slots_for_each_link = totalFreqSlot(each_dist,bandwidth)
        freq_slots+=(freq_slots_for_each_link*each_path_links[idx])
        
    return freq_slots,distance_segments
