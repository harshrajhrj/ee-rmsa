"""find regen nodes from a graph by selecting 20% of highest degree nodes
Block request if the path dist exceds optical reach by returning false"""


from math import ceil

OPTICAL_REACH = 4000 
REGENRESOURCESAVAILABLE=100



def no_of_regen_resources(lst, value):
    d = {}
    for item in lst:
        d[item] = value
    return d


def check_optical_reach_blocking_old(tree_path_dist, tree_path, regen_nodes,regen_node_limit, adj_mat):
    n_tree_path_dist = []
    n_tree_path = []
    regen_resource=regen_node_limit
    for i, dist in enumerate(tree_path_dist):
        path = tree_path[i]
        if dist > OPTICAL_REACH:
            regen_flag = False
            last_parent = True
            regen_dist = 0
            regen_node = 0
            for node in path:
                idx = path.index(node)
                if idx == 0:  # len(path)-1]:
                    continue
                if idx == len(path)-1:
                    prev_node = path[idx-1]
                    regen_dist += adj_mat[prev_node-1][node-1]
                    n_tree_path_dist.append(regen_dist)
                    n_tree_path.append(path[regen_node:]) 
                    last_parent = False
                else:
                    prev_node = path[idx-1]
                    # next_node=path[idx+1]
                    if node in regen_nodes and regen_resource[node]!=0:
                        regen_resource[node]-=1###############################################
                        regen_flag = True
                        prev_node_to_regen_dist = adj_mat[prev_node -
                                                          1][node-1] + regen_dist
                        # regen_node_to_next_dist=adj_mat[node-1][next_node-1]
                        n_tree_path_dist.append(prev_node_to_regen_dist)

                        # n_tree_path_dist.append(regen_node_to_next_dist)

                        n_tree_path.append(path[regen_node:idx+1])
                        regen_node = idx
                        regen_dist = 0
                        # n_tree_path.append(path[idx:])
                    else:
                        regen_dist += adj_mat[prev_node-1][node-1]

            if last_parent and regen_flag is False:
                n_tree_path_dist.append(dist)
                n_tree_path.append(path)
        else:
            n_tree_path_dist.append(dist)
            n_tree_path.append(path)

    print(n_tree_path_dist, n_tree_path)

    for dist in n_tree_path_dist:
        if dist > OPTICAL_REACH:
            return True

    regen_node_limit=regen_resource    
    return n_tree_path_dist, n_tree_path,regen_node_limit


def check_optical_reach_blocking(tree_path_dist, tree_path, regen_node_limit, adj_mat):
    n_tree_path_dist = []
    n_tree_path = []
    regen_happened=[]
    
    for i, dist in enumerate(tree_path_dist):
        past_dist = 0
        past_path = []
        future_dist = 0

        knowledge = 0
        path = tree_path[i]
        if dist > OPTICAL_REACH:
            #curr_dist=0
            for j in range(len(path) - 1):
                future_dist = adj_mat[path[j] - 1][path[j + 1] - 1]  # 3000
                knowledge = past_dist + future_dist  # 5000
                if knowledge > OPTICAL_REACH :
                    # regenerate at i inx
                    if(regen_node_limit[path[j]] == 0):
                        print("!!!!!  CAN'T REGENARATE Inavailability of regen resources at node: ",path[j])
                        return True
                    
                    past_path.append(path[j])
                    regen_happened.append(path[j])
                    n_tree_path_dist.append(past_dist)
                    n_tree_path.append(past_path)


                    past_dist = future_dist
                    past_path = []
                    past_path.append(path[j])

                    regen_node_limit[path[j]] -= 1

                else :
                    past_dist=knowledge
                    past_path.append(path[j])

            past_path.append(path[-1])
            n_tree_path_dist.append(past_dist)
            n_tree_path.append(past_path)


        else:
            n_tree_path_dist.append(dist)
            n_tree_path.append(path)
    
    return n_tree_path_dist, n_tree_path, regen_node_limit, regen_happened


