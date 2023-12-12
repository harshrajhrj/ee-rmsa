""" Consists of two function -- sTree: creates the steiner
 tree for the given adj matrix and the given request
dijkstra: finds min dist,min destination node,
 path between the source and the list of destinations. """

from sys import maxsize
import ast
# from ..request_blocking import OPTICAL_REACH


def pathSpliter(adj_matrix,  path, regeneration_node):
    regen_index = path.index(regeneration_node)
    path1 = path[:regen_index + 1]
    path2 = path[regen_index:]
    
    distance1 = sum(adj_matrix[path1[i] - 1][path1[i+1] - 1] for i in range(len(path1)-1))
    distance2 = sum(adj_matrix[path2[i] - 1][path2[i+1] - 1] for i in range(len(path2)-1))
    
    return ([distance1, distance2], [path1, path2])



def dijkstra(adj_matrix, start_node, destination_nodes, kth=0):

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

    
    node_distance_pairs = [(node, dist[node]) for node in destination_nodes]
    
    sorted_node_distance_pairs = sorted(node_distance_pairs, key=lambda x: x[1])


    min_node=sorted_node_distance_pairs[kth][0]
    min_dist=sorted_node_distance_pairs[kth][1]



    # return the minimum distance, the selected node, and the path from the start node to the selected node
    return min_dist, min_node, path[min_node]


def sTree(adjMat, request,regen_nodes,regen_resources):
    destinations=request[1]
    steiner_tree = {}
    tree_path_dist = []
    tree_path = []

    # step-1: Select the source node as the root;
    steiner_tree[request[0]] = []
    # request : [4, [5, 6]]

    while (len(destinations) != 0):
        closest_path = []
        shortest_dist = maxsize
        selected_tree_node = -1
        dest_node = request[1][0]

        # step-2: Select each node di from destination set D′, sequentially, and estimate the shortest path of each di from every node of the tree.
        # shortest dist path of di from every node of the tree
        for di in destinations:

            tryingdest=di;

            shortest_dist_di, selected_tree_node_di, path_di = dijkstra(
                adjMat, tryingdest-1, [i-1 for i in list(steiner_tree.keys())])
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

        #phase 2 checkif it exclude optical reach:---->
        if(shortest_dist > 4000):
            blocked = regeneration_inclusion(destinations,adjMat,steiner_tree,regen_nodes,regen_resources)
            if(blocked is True):
                return "The request is blocked"
                
            dist_parts,path_parts,regen_resources,destinations = blocked
            
            #include the segmented path in the tree.
            tree_path_dist.extend(dist_parts)
            tree_path.extend(path_parts)

            #update the Steiner tree dict
            for path in path_parts:
                key = request[0]
                for node in path:
                    if node in steiner_tree:
                        key = node
                    else:
                        steiner_tree[key].append(node)
                        steiner_tree[node] = []
                        if(node != dest_node):
                            key = node
        else:     

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

            destinations.remove(dest_node)

        # print("updated steiner tree: ",steiner_tree)

    return tree_path_dist, tree_path, steiner_tree

def regeneration_inclusion(destinations,adjMat,steiner_tree,regen_nodes,regen_resources):
    record = {}

    # initialize record vector
    for di in destinations:
        shortest_dist_di, selected_tree_node_di, path_di = dijkstra(adjMat, di-1, [i-1 for i in list(steiner_tree.keys())])
        path_di = [i+1 for i in path_di]
        record[di] =  [shortest_dist_di,path_di, 0]

    # Looping to get that regen fugg
    
    while(len(record)>0):
        print(record)
        #finding shortest dest
        min_record = min(record.items(), key=lambda item: item[1][0]) #form: (di,[distance,[path],kth-shortest])

        print("min_record = ",min_record)

        dest_node=min_record[0]
        path=min_record[1][1]
        for node in path: #checking only for single regeneration. try to implement for double and triple later...
            if node in regen_nodes: #found a regen node
                if regen_resources[node] > 0 : #regeneration resources available
                    #calculate and check length of each segments
                    distances,paths=pathSpliter(adjMat,path,node)
                    if(distances[0]<=4000 and distances[1] <= 4000):
                        regen_resources[node]-=1
                        destinations.remove(dest_node)
                        return distances, paths, regen_resources, destinations
                    
       

        record[dest_node][2]+=1

        #############################################################################################
        #how to break the loop 
        if(record[dest_node][2] + 1 > len(steiner_tree.keys())):
            del record[dest_node]
            continue


        #calculating next shortest path for shoartest dest node
        shortest_dist_di, selected_tree_node_di, path_di = dijkstra(
                adjMat, dest_node-1, [i-1 for i in list(steiner_tree.keys())], record[dest_node][2])
        
        path_di = [i+1 for i in path_di]
        
        #update record di with next shortest path
        record[dest_node][0]=shortest_dist_di
        record[dest_node][1]=path_di
    
    ##
    
    return True
    




        
        










    







adjacency_matrix = [
    [0, 3000, 0, 0, 0, 1100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3000, 0, 1100, 0, 0, 3700, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1100, 0, 1500, 3000, 0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1500, 0, 3000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3000, 3000, 0, 0, 0, 1200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1100, 3700, 0, 0, 0, 0, 1000, 0, 1200, 0, 1900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1000, 0, 0, 1000, 0, 1150, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1200, 0, 1150, 0, 0, 3800, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1200, 1000, 0, 0, 1100, 1400, 1200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3800, 1100, 0, 0, 0, 3700, 3500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1900, 0, 0, 1400, 0, 0, 3800, 0, 0, 1300, 0, 0, 0, 2600, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1200, 0, 3800, 0, 3800, 0, 0, 1100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3700, 0, 3800, 0, 2500, 0, 0, 1100, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3500, 0, 0, 2500, 0, 0, 0, 0, 1200, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1300, 0, 0, 0, 0, 0, 0, 0, 0, 1300, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1100, 0, 0, 0, 0, 1100, 0, 0, 0, 1000, 3000, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1100, 0, 0, 1100, 0, 3000, 0, 0, 0, 3500, 1000, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1200, 0, 0, 3000, 0, 0, 0, 0, 0, 0, 3800, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2600, 0, 0, 0, 0, 0, 0, 0, 0, 1200, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1300, 0, 0, 0, 1200, 0, 3800, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0, 3800, 0, 2000, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3000, 3500, 0, 0, 0, 2000, 0, 2200, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0, 0, 2200, 0, 3800],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3800, 0, 0, 0, 0, 3800, 0]
]

    
with open('requests.txt', 'r', encoding='utf-8') as file:
    request_str = file.read().rstrip()

graph_data = request_str.split('\n')



reg_nodes=[6, 7, 9, 11, 17]
regen_res={6: 100, 7: 100, 9: 100, 11: 100, 17: 100}
no_blocked=0
for i in graph_data:
    print(f"REQUEST = {i}")
    new_request = ast.literal_eval(i)
    stat=sTree(adjacency_matrix,new_request,reg_nodes,regen_res)
    print("stat= ",stat,"\n")
    if stat == "The request is blocked" :
        no_blocked+=1
        continue
    print("DONE REQUEST ...\n\n")

print("\n\n")
print("Number of blocked request : ",no_blocked, " of TOTAL REQUESTS : ", len(graph_data))
print(regen_res)
print("total regen happend = ",500- sum(regen_res.values()))