"""find regen nodes from a graph by selecting 20% of highest degree nodes
Block request if the path dist exceds optical reach by returning false"""

from itertools import combinations
from math import ceil
import sys


OPTICAL_REACH = 4000

max_int_value = sys.maxsize





def check_optical_reach_blocking_min_freqslot(
    tree_path_dist, tree_path, regen_node_limit, adj_mat, bw, max_reg_possible,regenerators
):
    n_tree_path_dist = []
    n_tree_path = []
    regen_happened = []

    for i, dist in enumerate(tree_path_dist):
        path = tree_path[i]
        if dist > OPTICAL_REACH:
            possible_reg_nodes = path[1:-1]
            number_of_regen = 1
            max_regen = len(possible_reg_nodes)
            while number_of_regen <= max_regen:
                min_slot_reg_nodes = possible_regenerate(
                    path,
                    adj_mat,
                    number_of_regen,
                    bw,
                    regen_node_limit,
                    max_reg_possible,
                    regenerators
                )

                if min_slot_reg_nodes == False:
                    if(max_reg_possible==regenerators):
                        return True
                    
                    max_reg_possible += 1
                    continue
                if min_slot_reg_nodes == True:
                    number_of_regen += 1
                else:
                    distance_list, path_list, regenerated_at = min_slot_reg_nodes
                    for dist_of in distance_list:
                        n_tree_path_dist.append(dist_of)
                    for one_path in path_list:
                        n_tree_path.append(one_path)
                    regen_happened.extend(regenerated_at)
                    for node in regenerated_at:
                        regen_node_limit[node] -= 1
                    break

            if number_of_regen == max_regen + 1:
                print("!!!!!  CAN'T REGENARATE at any point in path ")
                return True

        else:
            n_tree_path_dist.append(dist)
            n_tree_path.append(path)

    return (
        n_tree_path_dist,
        n_tree_path,
        regen_node_limit,
        regen_happened,
        max_reg_possible,
    )


# def totalFreqSlot(dist,bandwidth):
#     mf=0
#     if(2000<dist<=4000):
#         mf=1
#     elif 1000<dist<=2000 :
#         mf=2
#     elif 500<dist<=1000 :
#         mf=3
#     elif 0<dist<=500:
#         mf=4
#     num_slot=ceil(bandwidth/(12.5*mf))+GUARD
#     return num_slot

def sort_combinations(combination,node_values):
    values = [node_values[node] for node in combination]
    sum_values = sum(values)
    least_element = min(values, default=0)  # In case the combination is empty
    return (sum_values, least_element, combination)


def possible_regenerate(
    path, adj_mat, number_of_regen, bandwidth, regen_node_limit, max_reg,regenerator):
    possible_reg_nodes = path[1:-1]
    all_combinations = list(combinations(possible_reg_nodes, number_of_regen))

    all_combinations = sorted(all_combinations, key=lambda x: sort_combinations(x, regen_node_limit), reverse=True)

    distances = []
    paths = []
    regen_possible = False
    combination_used = []
    limit_reached = 0
    for each_comb in all_combinations:
        within_reg_capacity = True
        segmented_path = []
        current_sublist = []
        # for i in each_comb:
        #     if(regen_node_limit[i] == 0):
        #         continue

        for item in path:
            current_sublist.append(item)

            if item in each_comb:
                segmented_path.append(current_sublist)
                current_sublist = [item]

        if current_sublist:
            segmented_path.append(current_sublist)

        result = regeneration_stat(segmented_path, adj_mat)

        if result == True:
            continue
        for one_reg_node in each_comb:
            if regenerator - (regen_node_limit[one_reg_node] - 1) > max_reg:
                limit_reached += 1
                within_reg_capacity = False
        
        if(within_reg_capacity == False):
            continue
                

        dist_list = result
        distances = dist_list
        paths = segmented_path
        combination_used = list(each_comb)
        regen_possible = True
        return distances, paths, combination_used

    if regen_possible == False:
        if limit_reached > 0:
            return False
        return True
    else:
        return distances, paths, combination_used


def regeneration_stat(segmented_path, adj_mat):
    # find the distances of the segments
    distance_segments = []
    for each_path in segmented_path:
        past_dist = 0
        for j in range(len(each_path) - 1):
            seg = past_dist + adj_mat[each_path[j] - 1][each_path[j + 1] - 1]
            past_dist = seg
        distance_segments.append(seg)
    for each_dist in distance_segments:
        if each_dist > OPTICAL_REACH:
            return True
        # freq_slots += totalFreqSlot(each_dist,bandwidth)
    return distance_segments
