import steinerTree_creation as st
import request_blocking as rb
import findinNoOfSlot as fs
import energy_calculation as ec


# constans used : 1.NUMOFSLOT=300 #number of slots in each link [present in energy_calculation.py]
# 2.OPTICAL_REACH=3000 # max Optical reach should IS 3600 [present in request_blocking.py]
# 3.REGENRESOURCESAVAILABLE=100 [present in request_blocking.py]

#############################################################################################
# i) Open the file containing the adjacency matrix

import ast
with open('adjmat_USA.txt', 'r', encoding='utf-8') as f:
    contents = f.read()

rows = contents.split('\n')

adj_matrix = []

# Loop through each row of the matrix
for row in rows:
    # processing the data
    row = row.rstrip()
    values = row.split(' ')

    # Convert the values to integers
    values = [int(val) for val in values]

    # Add the row to the adjacency matrix
    adj_matrix.append(values)

print("Adj matrix is ready......")
# print(adj_matrix)

#############################################################################################
# degree of each node in the graph


def find_weighted_degrees(graph):
    n = len(graph)
    degrees = [0] * n

    for i in range(n):
        degree = 0
        for j in range(n):
            if graph[i][j] != 0:
                degree += graph[i][j]
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
print(slotsLink)

#############################################################################################
# finding regeneration nodes
regeneration_nodes = rb.highest_degree_regennodes(adj_matrix)
print("regeneration_nodes:", regeneration_nodes)

#############################################################################################
# availability of regeneration recources for each regeneration nodes.
regeneration_resources = rb.no_of_regen_resources(
    regeneration_nodes, rb.REGENRESOURCESAVAILABLE)
print("Available regeneration resources for each regen node: ",
      regeneration_resources)


#############################################################################################

# reading request from request.txt file

# total request=100
with open('requests.txt', 'r', encoding='utf-8') as file:
    request_str = file.read().rstrip()

request_list_str = request_str.split('\n')

#############################################################################################
# MAIN ALGO
# counters
num_blocked_request = 0
blocked_for_slot = 0
num_running_request = 0
tot_energy = 0


for one_request_str in request_list_str:

    # READING REQUEST
    # Convert the string to a list using ast.literal_eval()
    new_request = ast.literal_eval(one_request_str)
    print("request:", new_request)

    # CREATION OF STEINER TREE
    paths_dist, paths, steiner_tree = st.sTree(adj_matrix, new_request)
    print(paths_dist, paths, steiner_tree)

    # BLOCKING REQUEST WHICH ARE BEYOND OPTICAL REACH EVEN AFTER REGENERATING.
    # ALSO BLOCKED IF REGENERATION RESOURCES ARE ALL USED UP FOR THE REGENERATING NODE.
    blocked_or_new_tree = rb.check_optical_reach_blocking(
        paths_dist, paths, regeneration_nodes, regeneration_resources, adj_matrix)

    # BLOCKED REQUEST GETS FILTERED
    if blocked_or_new_tree is True:
        print("The request is blocked")
        num_blocked_request += 1

    else:  # GRANTING REQUESTS:
        regeneration_resources = blocked_or_new_tree[2]
        print("after updation of regen node: ", blocked_or_new_tree)

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
            print("request is blocked due to inavailability of slots")
            num_blocked_request += 1
            blocked_for_slot += 1
    print("\n\n")

# ANALYSIS PART 1
print("Total Blocked: Number of blocked request due to exceeding optical reach and cant be fixed by regeneration or inavailability of slots: ", num_blocked_request)
print("Number of request blocked due to exceeding optical reach: ",
      num_blocked_request-blocked_for_slot)
print("Blocked due to unavailability of slots in link: ", blocked_for_slot)
print("Number of running request : ", num_running_request)


print("After serving all the request the number of regeneration resources for each regeneration nodes: ", regeneration_resources)


#############################################################################################
#############################################################################################

# ANALYSIS PART 2:

# total energy:=
print(
    "Total energy for processing 100 requests [1.BVT, 2. Optical Amplifier, 3.OXV]:", tot_energy, "W")

# total slots required:=
print("total slots required for processing ", num_running_request,
      " requests: ", sum(sum(lst) for lst in slotsLink.values()))

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
