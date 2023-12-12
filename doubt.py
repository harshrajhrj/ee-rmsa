# """
# This module is just to test code before putting into origin.
# """
# from math import ceil
# from sys import maxsize
# from math import floor
# OPTICAL_REACH = 10
# NUMOFSLOTS=10

# mat = [
#     [0, 8, 0, 3, 6, 0],
#     [8, 0, 7, 7, 0, 6],
#     [0, 7, 0, 5, 0, 0],
#     [3, 7, 5, 0, 0, 0],
#     [6, 0, 0, 0, 0, 7],
#     [0, 6, 0, 0, 7, 0]
# ]
# request1 = [4, [5, 6]]

# def noOfSlots(bandwidth,dist_array):
#     guard=2
#     slots_arr=[]
#     for dist in dist_array:
#         path_slot=0
#         mf=0
#         if(dist>4800):
#             mf=1
#         elif 2400<dist<=4800 :
#             mf=2
#         elif 1200<dist<=2400 :
#             mf=3
#         else: 
#             mf=4
#         path_slot=ceil(bandwidth/(12.5*mf))+guard
#         slots_arr.append(path_slot)
#     return slots_arr

# def highest_degree_regennodes(adj_matrix):  # 20% of total nodes
#     # calculate the weighted degree of each node
#     weighted_degrees = [sum(row) for row in adj_matrix]

#     # sort the nodes in descending order of their degree
#     sorted_nodes = sorted(range(len(weighted_degrees)),
#                           key=lambda i: weighted_degrees[i], reverse=True)

#     # select the top ceil(20% of total nodes) of nodes with the highest degree
#     num_nodes = len(adj_matrix)
#     top_nodes = sorted_nodes[:ceil(num_nodes * 0.2)]

#     return top_nodes


# def dijkstra(adj_matrix, start_node, destination_nodes):
#     num_nodes = len(adj_matrix)
#     visited = [False] * num_nodes
#     dist = [maxsize] * num_nodes
#     path = [[]] * num_nodes

#     dist[start_node] = 0
#     path[start_node] = [start_node]

#     for _ in range(num_nodes):
#         # find the node with the minimum distance from the start node
#         min_dist = maxsize
#         min_node = -1
#         for j in range(num_nodes):
#             if not visited[j] and dist[j] < min_dist:
#                 min_dist = dist[j]
#                 min_node = j

#         if min_node == -1:
#             break

#         # visit the node with the minimum distance
#         visited[min_node] = True

#         # update the distances and paths of its neighbors
#         for j in range(num_nodes):
#             if adj_matrix[min_node][j] > 0:
#                 new_dist = dist[min_node] + adj_matrix[min_node][j]
#                 if new_dist < dist[j]:
#                     dist[j] = new_dist
#                     path[j] = [j] + path[min_node]

#     # find the minimum of the shortest distances from the start node to each of the destination nodes
#     min_dist = maxsize
#     min_node = -1
#     for node in destination_nodes:
#         if dist[node] < min_dist:
#             min_dist = dist[node]
#             min_node = node

#     # return the minimum distance, the selected node, and the path from the start node to the selected node
#     return min_dist, min_node, path[min_node]

#     # creating steiner tree for request 1


# def sTree(adjMat, request):
#     steiner_tree = {}
#     tree_path_dist = []
#     tree_path = []

#     # step-1: Select the source node as the root;
#     steiner_tree[request[0]] = []
#     # [4, [5, 6]]

#     while (len(request[1]) != 0):
#         closest_path = []
#         shortest_dist = 100
#         selected_tree_node = -1
#         dest_node = request[1][0]

#         # step-2: Select each node di from destination set D′, sequentially, and estimate the shortest path of each di from every node of the tree.
#         # shortest dist path of di from every node of the tree
#         for di in request[1]:

#             shortest_dist_di, selected_tree_node_di, path_di = dijkstra(
#                 adjMat, di-1, [i-1 for i in list(steiner_tree.keys())])

#             path_di = [i+1 for i in path_di]

#             print(shortest_dist_di, path_di)

#             if shortest_dist_di < shortest_dist:
#                 shortest_dist = shortest_dist_di
#                 closest_path = path_di
#                 dest_node = di
#                 selected_tree_node = selected_tree_node_di

#         # 1(c): Select the node d ∈ D′ having the minimum value of path length among all
#         # the shortest paths estimated in Step 1(b), and select the node x of the tree to which
#         # selected node di has the lowest shortest path.

#         # 1(d): Add a path between selected node d ∈ D′ i and the node x of the tree.
#         # if closest_node in tree.keys():
#         print(f"Adding node {dest_node} to tree")
#         tree_path_dist.append(shortest_dist)
#         tree_path.append(closest_path)

#         key = request[0]
#         for node in closest_path:
#             if node in steiner_tree:
#                 key = node
#             else:
#                 steiner_tree[key].append(node)
#                 steiner_tree[node] = []
#                 if(node != dest_node):
#                     key = node

#         request[1].remove(dest_node)

#         # print(steiner_tree)

#     return tree_path_dist, tree_path, steiner_tree


# # print(request1)
# #print(sTree(mat, request1))
# path_dist, path, steiner_tree = sTree(mat, request1)
# print(path_dist)
# regen_node = highest_degree_regennodes(mat)






# def regen_resources(lst, value):
#     d = {}
#     for item in lst:
#         d[item] = value
#     return d

# regen_limit=regen_resources(regen_node,100)





# # print(nodes_with_highest_degree_regennodes(mat))

# """ 1st algo most energy efficient: -------
# write a funtion which takes as input the above sTree outputs and calculate whether there exist a path in the tree which exceeds optical reach(4800)
# if it does the search for regen nodes(no. of regen resources at a node is cosidered infinity here) in the path--(for that assign 20% highest degree nodes as regen nodes in the tree ) now if regen nodes exist then okay check for distance again cosidering the regen node
# otherwise, block the whole request--> return 0 otherwise return 1
# calculate number of requests which are getting block 

# also calculate total energy taken for each request-- then give avg energy taken for ongoing request.--> for these we have to calculate total number of slots using the given formula for that calculate modulation format. also assing the slots(consider infinite no. of slots available)"""


# # print(check_optical_reach_blocking(path_dist,path,[5],mat))

# # def ak(a):
# #     if(a):
# #         return True

# #     return 1,a

# # print(ak(0))




# def check_optical_reach_blocking(tree_path_dist, tree_path, regen_nodes,regen_node_limit, adj_mat):
#     n_tree_path_dist = []
#     n_tree_path = []
#     for i, dist in enumerate(tree_path_dist):
#         path = tree_path[i]
#         if dist > OPTICAL_REACH:
#             regen_flag=False
#             regen_dist=0
#             regen_node=0
#             for node in path:
#                 idx = path.index(node)
#                 if idx == 0: #len(path)-1]:
#                     continue
#                 elif idx == len(path)-1:
#                     n_tree_path_dist.append(regen_dist)
#                     n_tree_path.append(path[regen_node:])
#                 else:
#                     prev_node = path[idx-1]
#                     # next_node=path[idx+1]
#                     if node in regen_nodes and regen_node_limit[node]!=0:#regeneration
#                         regen_node_limit[node]-=1
#                         regen_flag=True
#                         prev_node_to_regen_dist = adj_mat[prev_node-1][node-1] + regen_dist
#                         # regen_node_to_next_dist=adj_mat[node-1][next_node-1]
#                         n_tree_path_dist.append(prev_node_to_regen_dist)
                        
#                         # n_tree_path_dist.append(regen_node_to_next_dist)

#                         n_tree_path.append(path[regen_node:idx+1])
#                         regen_node=idx
#                         regen_dist=0
#                         # n_tree_path.append(path[idx:]) 
#                     else:
#                         regen_dist+= adj_mat[prev_node-1][node-1]   
                    
#             if regen_flag is False:
#                 n_tree_path_dist.append(dist)
#                 n_tree_path.append(path)
#         else:
#             n_tree_path_dist.append(dist)
#             n_tree_path.append(path)

#     print(n_tree_path_dist, n_tree_path)

#     for dist in n_tree_path_dist:
#         if dist>OPTICAL_REACH:
#             return True

    
#     return n_tree_path_dist, n_tree_path

# def create_slot_of_links(matrix):
#     link_lists = {}
#     for i in range(len(matrix)):
#         for j in range(i+1, len(matrix[0])):
#             if matrix[i][j] >0 :
#                 link = (i+1,j+1)

#                 link_lists[link] = [0 for k in range(NUMOFSLOTS)]
#     return link_lists 

# slotsLink=create_slot_of_links(mat)
# print(slotsLink)

# def assignSlots(slots_list,paths,link_mat):
#     for idx,tot_path in enumerate(paths):
#         slots=slots_list[idx]
#         tuple_list = [(tot_path[i], tot_path[i+1]) if tot_path[i] < tot_path[i+1] else (tot_path[i+1], tot_path[i]) for i in range(len(tot_path)-1)]
#         link_mat=find_sequence(link_mat,slots,tuple_list)
#     return link_mat

# def find_sequence(lists_dict, seq_length, keys):
#     n = len(lists_dict[keys[0]])
#     for i in range(n-seq_length+1):
#         if all(all(lists_dict[key][i+j] == 0 for key in keys) for j in range(seq_length)):
#             for key in keys:
#                 for j in range(seq_length):
#                     lists_dict[key][i+j] = 1
#             return lists_dict
#     return None

# def slotsEnergyBVT(slots,dist_arr):
#     tot_energy=0
#     for i,slot in enumerate(slots):
#         dist=dist_arr[i]
#         mf=0
#         if(dist>4800):
#             mf=1
#         elif 2400<dist<=4800 :
#             mf=2
#         elif 1200<dist<=2400 :
#             mf=3
#         else: 
#             mf=4
#         tm=12.5*mf
#         em=1.683*tm+91.333
#         path_energy=slot*em
#         tot_energy+=path_energy
#     return tot_energy

# def amplifier_energy(slots_list,paths,adj_matrix):
#     tot_energy=0
#     for idx,tot_path in enumerate(paths):
#         each_path_energy=0
#         slots=slots_list[idx]
#         tuple_list = [(tot_path[i], tot_path[i+1]) if tot_path[i] < tot_path[i+1] else (tot_path[i+1], tot_path[i]) for i in range(len(tot_path)-1)]
#         print(tuple_list)
#         for link in tuple_list:
#             link_length=adj_matrix[link[0]-1][link[1]-1]
#             print(link,"length: ",link_length)
#             amp_energy=floor(link_length/80 + 1)*100
#             print("energy for the link:",link,":",amp_energy)
#             each_path_energy+=amp_energy
#         print("tot energy for the path: ",each_path_energy)
#         tot_pow_given_slot=slots/NUMOFSLOTS*each_path_energy
#         print("it is using:  ",slots,"slots. Thus tot energy: ",tot_pow_given_slot)
#         tot_energy+=tot_pow_given_slot
#     return tot_energy



# energy_bvt=0

# print(regen_node)
# print(path_dist)
# print(check_optical_reach_blocking(path_dist, path, regen_node, regen_limit, mat))
# slots_arr=noOfSlots(100,path_dist)
# energy_bvt=slotsEnergyBVT(slots_arr,path_dist)
# print("energy =",energy_bvt)
# print(slots_arr)
# print(assignSlots(slots_arr,path,slotsLink))
# print("amp energy: ",amplifier_energy(slots_arr,path,mat))


with open('adjmat_4.txt', 'r', encoding='utf-8') as f:
    contents = f.read()

rows = contents.split('\n')

adj_matrix = []

# Loop through each row of the matrix
for row in rows:
    # processing the data
    #row = row.rstrip()
    
    # row=row.replace(",", "")
    values = row.split(', ')
    print(values)

    # Convert the values to integers
    values = [int(val) for val in values if val.strip()]

    # Add the row to the adjacency matrix
    adj_matrix.append(values)

print("Adj matrix is ready......")

print(len(adj_matrix))
# for i in adj_matrix:
#     print(i)