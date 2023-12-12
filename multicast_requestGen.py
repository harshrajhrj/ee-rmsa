import steinerTree_creation as st
import request_blocking as rb
import findinNoOfSlot as fs
import energy_calculation as ec
import generating_request_file as gr
import ast


# constans used : 1.NUMOFSLOT=300 #number of slots in each link [present in energy_calculation.py]
# 2.OPTICAL_REACH=4000 [present in request_blocking.py]
# 3.REGENRESOURCESAVAILABLE=100 [present in request_blocking.py]

#############################################################################################
# i) Open the file containing the adjacency matrix


with open('./NETWORKS/adjmat_1.txt', 'r', encoding='utf-8') as f: #'./NETWORKS/adjmat_1.txt'
    contents = f.read()

rows = contents.split('\n')

adj_matrix = []

# Loop through each row of the matrix
for row in rows:
    # processing the data
    
    values = row.split(', ')

    # Convert the values to integers
    values = [int(val) for val in values if val.strip()]

    # Add the row to the adjacency matrix
    adj_matrix.append(values)

print("\n\n\033[33m---: PRE-REQUISITES :---\033[0m")
print("Adjacency matrix of the Network is ready.")
#print(adj_matrix)

#############################################################################################
# degree of each node in the graph used for calculation of energy oxc


def find_weighted_degrees(graph):
    n = len(graph)
    degrees = [0] * n

    for i in range(n):
        degree = 0
        for j in range(n):
            if graph[i][j] != 0:
                degree += 1
        degrees[i] = degree

    return degrees


node_degree = find_weighted_degrees(adj_matrix)

#############################################################################################
# creating the slot matrix


def create_slot_of_links(matrix):
    link_lists = {}
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix[0])):
            if matrix[i][j] > 0:
                link = (i+1, j+1)

                link_lists[link] = [0 for k in range(ec.NUMOFSLOTS)]
    return link_lists


slotsLink = create_slot_of_links(adj_matrix)
print("Each link has",ec.NUMOFSLOTS,"slots")

#############################################################################################
# finding regeneration nodes
print("Each Regenerating node has",rb.REGENRESOURCESAVAILABLE,"resources.")
print("Optical Reach: ",rb.OPTICAL_REACH)
regeneration_nodes =list(range(1, len(adj_matrix) + 1))
print("Regeneration nodes are:", regeneration_nodes)

#############################################################################################
# availability of regeneration recources for each regeneration nodes.
regeneration_resources = rb.no_of_regen_resources(
    regeneration_nodes, rb.REGENRESOURCESAVAILABLE)
print("Available regeneration resources for each regen node: ",
      regeneration_resources)


#############################################################################################
# Generating request.txt
#gr.requestGen(len(adj_matrix),100)

#############################################################################################

# reading request from request.txt file

# total request=100
with open('requests.txt', 'r', encoding='utf-8') as file: #'requests.txt'
    request_str = file.read().rstrip()

request_list_str = request_str.split('\n')

#############################################################################################
# MAIN ALGO
# counters
num_blocked_request = 0
blocked_for_slot = 0
num_running_request = 0
tot_energy = 0

print("\n\033[35m############################################################################################################################...\033[0m")

print("\n\n\033[33m----: DYNAMIC REQUESTS ARE SESRVED AS FOLLOWS :----\033[0m\n\n")

for one_request_str in request_list_str:

    # READING REQUEST
    # Convert the string to a list using ast.literal_eval()
    new_request = ast.literal_eval(one_request_str)
    print("\033[36mRequest:", new_request,"\033[0m")

    # CREATION OF STEINER TREE
    paths_dist, paths, steiner_tree = st.sTree(adj_matrix, new_request)
    print("\n\033[32mCREATING STEINER TREE...\033[0m")
    print("All the segment present in the Tree: ",paths)
    print("Total Distance of each respective segments: ",paths_dist)
    print("The Steiner Tree: ", steiner_tree)

    print("\n\033[32mCHECKING FOR REGENERATION:---\033[0m")
    # BLOCKING REQUEST WHICH ARE BEYOND OPTICAL REACH EVEN AFTER REGENERATING.
    # ALSO BLOCKED IF REGENERATION RESOURCES ARE ALL USED UP FOR THE REGENERATING NODE.
    # returns path_dist, paths
    blocked_or_new_tree = rb.check_optical_reach_blocking(
        paths_dist, paths, regeneration_resources, adj_matrix)

    # BLOCKED REQUEST GETS FILTERED // Regeneration resouce unavailability or regeneration not not available 
    if blocked_or_new_tree is True:
        print("The request is blocked")
        num_blocked_request += 1

    else:  # GRANTING REQUESTS:

        #print("after updation of regen node: ", blocked_or_new_tree)
        print("All the segment present in the Tree after Regeneration: ",blocked_or_new_tree[1])
        print("Total Distance of each respective segments: ",blocked_or_new_tree[0])
        print("Regeneration happened at nodes: ",blocked_or_new_tree[3])


        regeneration_resources = blocked_or_new_tree[2] #Remaining regeneration resources in each regenerating node

        # FINDING NO. OF SLOTS REQUIRED AS PER THE BANDWIDTH OF THE REQUEST AND DIST OF EACH S.TREE PATH
        slots_required = fs.noOfSlots(new_request[2], blocked_or_new_tree[0])
        print("No. of slots required for each path: ", slots_required)
        

        # ASSIGN THE REQUIRED SLOTS IF AVAILABLE OR BLOCK REQUEST
        psudoSlotsLink = fs.assignSlots(
            slots_required, blocked_or_new_tree[1], slotsLink)
        if psudoSlotsLink is not None:
            print("The corrosponding slots are assigned..")
            num_running_request += 1
            slotsLink = psudoSlotsLink

            # ENERGY USED: TO SERVE THE REQUEST
            energy_bvt = ec.slotsEnergyBVT(
                slots_required, blocked_or_new_tree[0])
            energy_opticalAmp = ec.amplifier_energy(
                slots_required, blocked_or_new_tree[1], adj_matrix)
            energy_oxc = ec.crossConnect_energy(
                slots_required, blocked_or_new_tree[1], node_degree)
            print("TOTAL ENERGY USED BY THE REQUEST: ",
                  energy_oxc+energy_bvt+energy_opticalAmp)

            tot_energy += energy_bvt
            tot_energy += energy_opticalAmp
            tot_energy += energy_oxc
        else:
            print("Request is blocked due to inavailability of slots")
            num_blocked_request += 1
            blocked_for_slot += 1
    print("\n\n")

# ANALYSIS PART 1

print("\033[33m----:ALL THE REQUESTS ARE PROCESSED SUCCESSFULLY:----\033[0m\n\n")


print("\033[35m############################################################################################################################...\033[0m")
print("\n\033[33m----:ANALYSIS:----\033[0m\n")
print("Total Blocked: Number of blocked request inavailability of slots: ", num_blocked_request)
print("Number of request blocked due to exceeding optical reach: ",
      num_blocked_request-blocked_for_slot)
print("Blocked due to unavailability of slots in link: ", blocked_for_slot)
print("Number of running request : ", num_running_request)
print("Total number of Regeneration Happened = ",len(adj_matrix)*rb.REGENRESOURCESAVAILABLE - sum(regeneration_resources.values()))


print("After serving all the request the number of regeneration resources for each regeneration nodes: ", regeneration_resources)


#############################################################################################

# ANALYSIS PART 2:

# total energy:=
print(
    "Total energy for processing 100 requests [1.BVT, 2. Optical Amplifier, 3.OXV]:", tot_energy, "W")

# total slots required:=
total_slots_used = sum(sum(lst) for lst in slotsLink.values())
print("total slots required for processing ", num_running_request,
      " requests: ", total_slots_used)

print("Spectrum Efficiency :: (total frequency slot used / total number of request served) = ", total_slots_used/num_running_request)

#bandwidth_blocking_ratio=

# max regeneration at which node:=
max_regen_node = min(regeneration_resources, key=regeneration_resources.get)
max_regen_time = rb.REGENRESOURCESAVAILABLE - \
    regeneration_resources[max_regen_node]
print(
    f"Maximum number of regeneration occured at node: {max_regen_node} which is {max_regen_time} times.")

# highest number of frequency slots used by
max_link, max_count = max(slotsLink.items(), key=lambda item: item[1].count(1))
print(
    f"Highest number of slots is used by link {max_link} which is {max_count.count(1)}")
