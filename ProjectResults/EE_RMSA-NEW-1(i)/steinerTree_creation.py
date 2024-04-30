""" Consists of two function -- sTree: creates the steiner
 tree for the given adj matrix and the given request
dijkstra: finds min dist,min destination node,
 path between the source and the list of destinations. """

from sys import maxsize


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
    min_dist = maxsize
    min_node = -1
    for node in destination_nodes:
        if dist[node] < min_dist:
            min_dist = dist[node]
            min_node = node

    # return the minimum distance, the selected node, and the path from the start node to the selected node
    return min_dist, min_node, path[min_node]


def sTree(adjMat, request):
    steiner_tree = {}
    tree_path_dist = []
    tree_path = []

    # step-1: Select the source node as the root;
    steiner_tree[request[0]] = []
    # request : [4, [5, 6]]

    while (len(request[1]) != 0):
        closest_path = []
        shortest_dist = maxsize
        selected_tree_node = -1
        dest_node = request[1][0]

        # step-2: Select each node di from destination set D′, sequentially, and estimate the shortest path of each di from every node of the tree.
        # shortest dist path of di from every node of the tree
        for di in request[1]:

            shortest_dist_di, selected_tree_node_di, path_di = dijkstra(
                adjMat, di-1, [i-1 for i in list(steiner_tree.keys())])
            path_di = [i+1 for i in path_di]

            # print(shortest_dist_di,path_di)

            if shortest_dist_di < shortest_dist:
                shortest_dist = shortest_dist_di
                closest_path = path_di
                dest_node = di
                selected_tree_node = selected_tree_node_di
  
    

        # 1(c): Select the node d ∈ D′ having the minimum value of path length among all
        # the shortest paths estimated in Step 1(b), and select the node x of the tree to which
        # selected node di has the lowest shortest path.
        # 1(d): Add a path between selected node d ∈ D′ i and the node x of the tree.

        # print(f"Adding node {dest_node} to tree as its distance from the tree is minimum.\n")

        tree_path_dist.append(shortest_dist)
        tree_path.append(closest_path)

        key = request[0]
        # print("closest path: ",closest_path," is added to tree.")
        for node in closest_path:
            if node in steiner_tree:
                key = node
            else:
                steiner_tree[key].append(node)
                steiner_tree[node] = []
                if(node != dest_node):
                    key = node

        request[1].remove(dest_node)

        # print("updated steiner tree: ",steiner_tree)

    return tree_path_dist, tree_path, steiner_tree
