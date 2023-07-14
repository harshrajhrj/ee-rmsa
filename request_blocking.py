"""find regen nodes from a graph by selecting 20% of highest degree nodes
Block request if the path dist exceds optical reach by returning false"""


from math import ceil

OPTICAL_REACH = 3600
REGENRESOURCESAVAILABLE=10


def highest_degree_regennodes(adj_matrix):  # 20% of total nodes
    # calculate the weighted degree of each node
    weighted_degrees = [sum(row) for row in adj_matrix]

    # sort the nodes in descending order of their degree
    sorted_nodes = sorted(range(len(weighted_degrees)),
                          key=lambda i: weighted_degrees[i], reverse=True)

    # select the top ceil(20% of total nodes) of nodes with the highest degree
    num_nodes = len(adj_matrix)
    top_nodes = sorted_nodes[:ceil(num_nodes * 0.2)]

    return top_nodes

def no_of_regen_resources(lst, value):
    d = {}
    for item in lst:
        d[item] = value
    return d


def check_optical_reach_blocking(tree_path_dist, tree_path, regen_nodes,regen_node_limit, adj_mat):
    n_tree_path_dist = []
    n_tree_path = []
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
                    if node in regen_nodes and regen_node_limit[node]!=0:
                        regen_node_limit[node]-=1
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

    return n_tree_path_dist, n_tree_path,regen_node_limit
