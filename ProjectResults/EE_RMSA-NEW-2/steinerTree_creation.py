""" Consists of two function -- sTree: creates the steiner
 tree for the given adj matrix and the given request
dijkstra: finds min dist,min destination node,
 path between the source and the list of destinations. """

from itertools import combinations
from sys import maxsize


OPTICAL_REACH = 4000


def dijkstra(adj_matrix, start_node, destination_nodes):
    num_nodes = len(adj_matrix)
    visited = [False] * num_nodes
    dist = [maxsize] * num_nodes
    path = [[]] * num_nodes

    dist[start_node] = 0
    path[start_node] = [start_node]

    for _ in range(num_nodes):
        # find the node with the minimum distance from the start node
        min_dist = maxsize
        min_node = -1
        for j in range(num_nodes):
            if not visited[j] and dist[j] < min_dist:
                min_dist = dist[j]
                min_node = j

        if min_node == -1:
            break

        # visit the node with the minimum distance
        visited[min_node] = True

        # update the distances and paths of its neighbors
        for j in range(num_nodes):
            if adj_matrix[min_node][j] > 0:
                new_dist = dist[min_node] + adj_matrix[min_node][j]
                if new_dist < dist[j]:
                    dist[j] = new_dist
                    path[j] = [j] + path[min_node]

    # find the minimum of the shortest distances from the start node to each of the destination nodes
    # min_dist = maxsize
    # min_node = -1
    # for node in destination_nodes:
    #     if dist[node] < min_dist:
    #         min_dist = dist[node]
    #         min_node = node

    # return the minimum distance, the selected node, and the path from the start node to the selected node
    # return min_dist, min_node, path[min_node]
    result_distances = [dist[node] for node in destination_nodes]
    result_paths = [path[node] for node in destination_nodes]

    return result_distances, result_paths


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

def sort_combinations(combination,node_values):
    values = [node_values[node] for node in combination]
    sum_values = sum(values)
    least_element = min(values, default=0)  # In case the combination is empty
    return (sum_values, least_element, combination)

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


def sTree(adjMat, request, regen_node_limit,max_regeneration,regenerator):
    steiner_tree = {}
    tree_path_dist = []
    tree_path = []
    regen_happened = []
    regen_node_copy = dict(regen_node_limit)

    # step-1: Select the source node as the root;
    steiner_tree[request[0]] = []
    # request : [4, [5, 6]]

    number_of_regen = 1
    while len(request[1]) != 0:
        closest_path = []
        shortest_dist = maxsize
        selected_tree_node = -1
        dest_node = request[1][0]
        ulimate_list_dist = []
        ultimate_list_path = []
        

        # step-2: Select each node di from destination set D′, sequentially, and estimate the shortest path of each di from every node of the tree.
        # shortest dist path of di from every node of the tree
        for di in request[1]:
            # shortest_dist_di, selected_tree_node_di, path_di = dijkstra( #single source shortest path for one dest di to all the present nodes in steiner tree
            #     adjMat, di-1, [i-1 for i in list(steiner_tree.keys())])
            # path_di = [i+1 for i in path_di]

            shortest_dist_list, shortest_path_list = dijkstra(
                adjMat, di - 1, [i - 1 for i in list(steiner_tree.keys())]
            )
            for path in shortest_path_list:
                path[:] = [node + 1 for node in path]
            # the list of shortest distance connecting the destination node di with any node of the tree: shortest_dist_list
            # the list of corrorsponding paths. Both of these lists are indexed in the same order.
            ulimate_list_dist.append(shortest_dist_list)
            ultimate_list_path.append(shortest_path_list)

            # print(shortest_dist_di,path_di)

            # if shortest_dist_di < shortest_dist:
            #     shortest_dist = shortest_dist_di
            #     closest_path = path_di
            #     dest_node = di
            #     selected_tree_node = selected_tree_node_di

        # 1(c): Select the node d ∈ D′ having the minimum value of path length among all
        # the shortest paths estimated in Step 1(b), and select the node x of the tree to which
        # selected node di has the lowest shortest path.
        # 1(d): Add a path between selected node d ∈ D′ i and the node x of the tree.

        # print(f"Adding node {dest_node} to tree as its distance from the tree is minimum.\n")

        # CHECKING FOR CORRECT REGENERATION AND HENCE MODIFYING THE TREE\\\\--LOOP HERE--\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            # print(di,"-->",ulimate_list_dist)
            # print()
        work_done = 0
        n_tree_path_dist = []
        n_tree_path = []
        regen_happened_dumy=[]

        within_reg_capacity = False

        while (len(ulimate_list_dist)!=0):
            
            shortest_dist, (idx_row, idx_col) = min(
                (min(row), (idx, row.index(min(row))))
                for idx, row in enumerate(ulimate_list_dist)
            )
            closest_path = ultimate_list_path[idx_row][idx_col]
            dest_node = closest_path[-1]
            
            if shortest_dist <= OPTICAL_REACH:
                tree_path_dist.append(shortest_dist)
                tree_path.append(closest_path)
                steiner_tree = appendPathtoTree(steiner_tree, closest_path)
                number_of_regen = 1
                break
            # *88888888888888888888888888888888888888888888888888888888888888888888888
            destination_added = False
            possible_reg_nodes = closest_path[1:-1]
            all_combinations = list(combinations(possible_reg_nodes, number_of_regen))
            all_combinations = sorted(all_combinations, key=lambda x: sort_combinations(x, regen_node_copy), reverse=True)


            # result_dict = {key: regen_node_limit[key] for key in possible_reg_nodes}
            # sorted_result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
            # keys = list(sorted_result_dict.keys())

            

            for each_comb in all_combinations:
                cannot_reg_flag = False
                segmented_path = []
                current_sublist = []
                for item in closest_path:
                    current_sublist.append(item)

                    if item in each_comb:
                        segmented_path.append(current_sublist)
                        current_sublist = [item]
                if current_sublist:
                    segmented_path.append(current_sublist)
                result = regeneration_stat(segmented_path, adjMat)
                if(result == True):
                    continue
                for one_reg_node in each_comb:
                    if regenerator - (regen_node_copy[one_reg_node] - 1) > max_regeneration:
                    # limit_reached += 1
                        within_reg_capacity = True
                        cannot_reg_flag=True
                        

                if(cannot_reg_flag == True):
                    continue
        
                
                #REGENERATION
                for one_reg_node in each_comb:
                    regen_happened.append(one_reg_node)
                    regen_node_copy[one_reg_node]-=1

                tree_path_dist.extend(result)
                tree_path.extend(segmented_path)

                for each_path in segmented_path:
                    steiner_tree = appendPathtoTree(steiner_tree, each_path)
                destination_added=True
                number_of_regen = 1
                break


            if(destination_added == False):
                #OUT OF FOR LOOP WITHOUT REGENERATION
                del ulimate_list_dist[idx_row][idx_col]
                del ultimate_list_path[idx_row][idx_col]
                if not ulimate_list_dist[idx_row]:  # Remove the inner list if it becomes empty
                    del ulimate_list_dist[idx_row]
                if not ultimate_list_path[idx_row]:  # Remove the inner list if it becomes empty
                    del ultimate_list_path[idx_row]
                continue
            else:
                break
            
        else:
            if within_reg_capacity==True:
                if(max_regeneration==regenerator):
                    return True
                max_regeneration +=1
                continue
            else: 
                print("Have to do more then one regenration.")
                # return True;
                number_of_regen+=1
                continue

            

        

        request[1].remove(dest_node)        

                
                
                
            # *88888888888888888888888888888888888888888888888888888888888888888888888
            # finding the nodes to be regenerated
            # future_dist = 0
            # knowledge = 0
            # past_dist = 0
            # past_path = []

            # path = closest_path
            # n_tree_path_dist = []
            # n_tree_path = []
            # regen_happened_dumy=[]
            # for j in range(len(path) - 1):
            #     future_dist = adjMat[path[j] - 1][path[j + 1] - 1]  # 3000
            #     knowledge = past_dist + future_dist  # 5000
            #     if knowledge > OPTICAL_REACH:
            #         regen_node_copy = dict(regen_node_limit)
            #         regen_node_copy[path[j]] -= 1
            #         if regen_node_limit[path[j]] == 0 or MAXDIFFATREG < max(
            #             regen_node_copy.values()
            #         ) - min(regen_node_copy.values()):
            #             # print("!!!!!  CAN'T REGENARATE Inavailability of regen resources at node: ",path[j])
            #             del ulimate_list_dist[idx_row][idx_col]
            #             del ultimate_list_path[idx_row][idx_col]
            #             if not ulimate_list_dist[
            #                 idx_row
            #             ]:  # Remove the inner list if it becomes empty
            #                 del ulimate_list_dist[idx_row]
            #             if not ultimate_list_path[
            #                 idx_row
            #             ]:  # Remove the inner list if it becomes empty
            #                 del ultimate_list_path[idx_row]
            #             cannot_reg_flag = 1
            #             break
            #         else:  # regenerate
            #             past_path.append(path[j])
            #             n_tree_path_dist.append(past_dist)
            #             n_tree_path.append(past_path)
            #             regen_happened_dumy.append(path[j])

            #             past_dist = future_dist
            #             past_path = []
            #             past_path.append(path[j])

            #     else:
            #         past_dist = knowledge
            #         past_path.append(path[j])

            # if cannot_reg_flag == 0:  # regeneration took place
            #     regen_node_limit = dict(regen_node_copy)
            #     past_path.append(path[-1])
            #     n_tree_path_dist.append(past_dist)
            #     n_tree_path.append(past_path)

            #     regen_happened = regen_happened_dumy
            #     for dst in n_tree_path_dist:
            #         tree_path_dist.append(dst)
            #     for pth in n_tree_path:
            #         tree_path.append(pth)
            #         steiner_tree = appendPathtoTree(steiner_tree, pth)

            #     work_done = 1
            #     break

        # else:
        #     if within_reg_capacity==True:
        #         max_regeneration+=1
        #         continue
        #     else: 
        #         print("Have to do more then one regenration.")
        #         return True;

            

        # if work_done == 0:#include dest which dosent exceeds OPTICAL REACH.
        #     tree_path_dist.append(shortest_dist)
        #     tree_path.append(closest_path)

        #     # print("closest path: ",closest_path," is added to tree.")

        #     steiner_tree = appendPathtoTree(steiner_tree, closest_path)

        # request[1].remove(dest_node)

        # print("updated steiner tree: ",steiner_tree)
    regen_node_limit=regen_node_copy

    return tree_path_dist, tree_path, regen_node_limit, regen_happened,steiner_tree,max_regeneration


def appendPathtoTree(stree, closest_path):
    dest_node = closest_path[-1]
    for node in closest_path:
        if node in stree:
            key = node
        else:
            stree[key].append(node)
            stree[node] = []
            if node != dest_node:
                key = node
    return stree




# for reg in keys:
            #     current_sublist = []
            #     segmented_path=[]
            #     for item in closest_path:
            #         current_sublist.append(item)

            #         if item==reg:
            #             segmented_path.append(current_sublist)
            #             current_sublist = [item]
            #     if current_sublist:
            #         segmented_path.append(current_sublist)
                
            #     result = regeneration_stat(segmented_path, adjMat)

            #     if(result == True):
            #         continue  #the inner segments are out of optical reach
            #     if REGENRESOURCESAVAILABLE - (regen_node_copy[reg] - 1) > max_regeneration:
            #         # limit_reached += 1
            #         within_reg_capacity = True
            #         continue