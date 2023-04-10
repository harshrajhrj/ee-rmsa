import sys
mat = [
    [0, 8, 0, 3, 6, 0],
    [8, 0, 7, 7, 0, 6],
    [0, 7, 0, 5, 0, 0],
    [3, 7, 5, 0, 0, 0],
    [6, 0, 0, 0, 0, 7],
    [0, 6, 0, 0, 7, 0]
]
request1 = [6, [1, 4]]





def dijkstra(adj_matrix, start_node, destination_nodes):
    num_nodes = len(adj_matrix)
    visited = [False] * num_nodes
    dist = [sys.maxsize] * num_nodes
    path = [[]] * num_nodes
    
    dist[start_node] = 0
    path[start_node] = [start_node]
    
    for _ in range(num_nodes):
        # find the node with the minimum distance from the start node
        min_dist = sys.maxsize
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
                    path[j] =  [j] + path[min_node] 
    
    # find the minimum of the shortest distances from the start node to each of the destination nodes
    min_dist = sys.maxsize
    min_node = -1
    for node in destination_nodes:
        if dist[node] < min_dist:
            min_dist = dist[node]
            min_node = node
    
    # return the minimum distance, the selected node, and the path from the start node to the selected node
    return min_dist, min_node, path[min_node]

 
# creating steiner tree for request 1
steiner_tree = {}

# step-1: Select the source node as the root;
steiner_tree[request1[0]] = []
# [4, [5, 6]]

while (len(request1[1]) != 0):
    closest_path= []
    shortest_dist = 100
    selected_tree_node=-1
    dest_node = request1[1][0]

    # step-2: Select each node di from destination set D′, sequentially, and estimate the shortest path of each di from every node of the tree.
    # shortest dist path of di from every node of the tree
    for di in request1[1]:

        shortest_dist_di,selected_tree_node_di, path_di = dijkstra(mat, di-1, [i-1 for i in list(steiner_tree.keys())])
        # path_di=path_di[::-1]
        path_di=[i+1 for i in path_di]

        print(shortest_dist_di,path_di)
        

        if shortest_dist_di < shortest_dist:
            shortest_dist = shortest_dist_di
            closest_path = path_di
            dest_node = di
            selected_tree_node=selected_tree_node_di
        

    # 1(c): Select the node d ∈ D′ having the minimum value of path length among all
    # the shortest paths estimated in Step 1(b), and select the node x of the tree to which
    # selected node di has the lowest shortest path.

    # 1(d): Add a path between selected node d ∈ D′ i and the node x of the tree.
    # if closest_node in tree.keys():
    print(f"Adding node {dest_node} to tree")

    current_node=steiner_tree
    key=request1[0]
    for node in closest_path:
        if node in steiner_tree:
            key=node
        else:
            if(node==dest_node):
                steiner_tree[key].append(node)
                steiner_tree[node]=[]
            else:
                steiner_tree[key].append(node)
                steiner_tree[node]=[]
                key=node


    request1[1].remove(dest_node)

    # print(steiner_tree)
    


print(steiner_tree)
