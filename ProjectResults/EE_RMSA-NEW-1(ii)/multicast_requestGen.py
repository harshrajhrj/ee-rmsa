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


def create_slot_of_links(matrix,slots):
    link_lists = {}
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix[0])):
            if matrix[i][j] > 0:
                link = (i+1, j+1)

                link_lists[link] = [0 for k in range(slots)]
    return link_lists

def no_of_regen_resources(lst, value):
    d = {}
    for item in lst:
        d[item] = value
    return d

def main(request_list,regenerators,slotsNo,totReqSlot):
    with open('./EE_RMSA-NEW-1(ii)/NETWORKS/adjmat_1.txt', 'r', encoding='utf-8') as f: #'./NETWORKS/adjmat_1.txt'
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

    # print("\n\n\033[33m---: PRE-REQUISITES :---\033[0m")
    # print("Adjacency matrix of the Network is ready.")
    #print(adj_matrix)

    #############################################################################################
    # degree of each node in the graph used for calculation of energy oxc





    node_degree = find_weighted_degrees(adj_matrix)

    #############################################################################################
    # creating the slot matrix




    slotsLink = create_slot_of_links(adj_matrix, slotsNo)
    # print(slotsLink)
    # print("Each link has",ec.NUMOFSLOTS,"slots")

    #############################################################################################
    # finding regeneration nodes
    max_regeneration = 1
    # print("Each Regenerating node has",rb.REGENRESOURCESAVAILABLE,"resources.")
    # print("Optical Reach: ",rb.OPTICAL_REACH)
    regeneration_nodes =list(range(1, len(adj_matrix) + 1))
    # print("Regeneration nodes are:", regeneration_nodes)

    #############################################################################################
    # availability of regeneration recources for each regeneration nodes.
    regeneration_resources = no_of_regen_resources(
        regeneration_nodes, regenerators)
    # print("Available regeneration resources for each regen node: ",regeneration_resources)


    #############################################################################################
    # Generating request.txt
    #gr.requestGen(len(adj_matrix),100)

    #############################################################################################

    # reading request from request.txt file

    # total request=100
    with open(request_list, 'r', encoding='utf-8') as file: #'requests.txt'
        request_str = file.read().rstrip()

    request_list_str = request_str.split('\n')

    #############################################################################################
    # MAIN ALGO
    # counters
    num_blocked_request = 0
    blocked_for_slot = 0
    num_running_request = 0
    tot_energy = 0

    # print("\n\033[35m############################################################################################################################...\033[0m")

    # print("\n\n\033[33m----: DYNAMIC REQUESTS ARE SESRVED AS FOLLOWS :----\033[0m\n\n")
    tot_requests = len(request_list_str)

    for one_request_str in request_list_str:

        # READING REQUEST
        # Convert the string to a list using ast.literal_eval()
        new_request = ast.literal_eval(one_request_str)
        # print("\033[36mRequest:", new_request,"\033[0m")

        # CREATION OF STEINER TREE
        paths_dist, paths, steiner_tree = st.sTree(adj_matrix, new_request)
        # print("\n\033[32mCREATING STEINER TREE...\033[0m")
        # print("All the segment present in the Tree: ",paths)
        # print("Total Distance of each respective segments: ",paths_dist)
        # print("The Steiner Tree: ", steiner_tree)

        # print("\n\033[32mCHECKING FOR REGENERATION:---\033[0m")
        # BLOCKING REQUEST WHICH ARE BEYOND OPTICAL REACH EVEN AFTER REGENERATING.
        # ALSO BLOCKED IF REGENERATION RESOURCES ARE ALL USED UP FOR THE REGENERATING NODE.
        # returns path_dist, paths
        bandW = new_request[2]
        regeneration_resources_copy=regeneration_resources.copy()
        blocked_or_new_tree = rb.check_optical_reach_blocking_min_freqslot(
            paths_dist, paths, regeneration_resources_copy, adj_matrix,bandW,max_regeneration,regenerators)

        # BLOCKED REQUEST GETS FILTERED // Regeneration resouce unavailability or regeneration not not available 
        if blocked_or_new_tree is True:
            # print("The request is blocked due to inavailability of regeneration resources")
            num_blocked_request += 1

        else:  # GRANTING REQUESTS:

            #print("after updation of regen node: ", blocked_or_new_tree)
            # print("All the segment present in the Tree after Regeneration: ",blocked_or_new_tree[1])
            # print("Total Distance of each respective segments: ",blocked_or_new_tree[0])
            # print("Regeneration happened at nodes: ",blocked_or_new_tree[3])
            # print("Max regeneration : ",blocked_or_new_tree[4])
            # print("Regenerating Resources: ",blocked_or_new_tree[2])

            #Remaining regeneration resources in each regenerating node
            
            # FINDING NO. OF SLOTS REQUIRED AS PER THE BANDWIDTH OF THE REQUEST AND DIST OF EACH S.TREE PATH
            slots_required = fs.noOfSlots(new_request[2], blocked_or_new_tree[0])
            # print("No. of slots required for each path: ", slots_required)
            # for a in slotsLink:
            #     print(a,":",slotsLink[a].count(1))
            

            # ASSIGN THE REQUIRED SLOTS IF AVAILABLE OR BLOCK REQUEST
            slotsLinkCopy = slotsLink.copy()
            psudoSlotsLink = fs.assignSlots(
                slots_required, blocked_or_new_tree[1], slotsLinkCopy)
            if psudoSlotsLink is True:
                # print("Request is blocked due to inavailability of slots")
                num_blocked_request += 1
                blocked_for_slot += 1
            else:
                regeneration_resources = blocked_or_new_tree[2]
                max_regeneration = blocked_or_new_tree[4]
                # print("The corrosponding slots are assigned..")
                num_running_request += 1
                slotsLink = psudoSlotsLink

                # ENERGY USED: TO SERVE THE REQUEST
                energy_bvt = ec.slotsEnergyBVT(
                    slots_required, blocked_or_new_tree[0])
                energy_opticalAmp = ec.amplifier_energy(
                    slots_required, blocked_or_new_tree[1], adj_matrix,slotsNo)
                energy_oxc = ec.crossConnect_energy(
                    slots_required, blocked_or_new_tree[1], node_degree,slotsNo)
                # print("TOTAL ENERGY USED BY THE REQUEST: ",energy_oxc+energy_bvt+energy_opticalAmp)

                tot_energy += energy_bvt
                tot_energy += energy_opticalAmp
                tot_energy += energy_oxc
        # print("\n\n")

    # ANALYSIS PART 1

    # print("\033[33m----:ALL THE REQUESTS ARE PROCESSED SUCCESSFULLY:----\033[0m\n\n")


    # print("\033[35m############################################################################################################################...\033[0m")
    print("\n\033[33m----:ANALYSIS:----ALGO 3----\033[0m\n")
    # print("Total Requests: ",tot_requests)
    # print("Total Blocked: Number of blocked request inavailability of slots: ", num_blocked_request)
    # print("Number of request blocked due to exceeding optical reach: ",
    #     num_blocked_request-blocked_for_slot)
    # print("Blocked due to unavailability of slots in link: ", blocked_for_slot)
    # print("Number of running request : ", num_running_request)
    # print("Total number of Regeneration Happened = ",len(adj_matrix)*rb.REGENRESOURCESAVAILABLE - sum(regeneration_resources.values()))


    # print("After serving all the request the number of regeneration resources for each regeneration nodes: ", regeneration_resources)


    #############################################################################################

    # ANALYSIS PART 2:
    print(f"\033[35mTotal Blocked:  {num_blocked_request}\033[0m")
    blocking_prob = num_blocked_request/tot_requests
    print(f"\033[35mBlocking Probablity: {blocking_prob}\033[0m")

    # Bandwidth Blocking Ratio = Total Blocked BW slots / Total Requested BW slots
    total_slots_used = sum(sum(lst) for lst in slotsLink.values())
    print(f"\033[35mBandwidth Blocking Ratio: {(totReqSlot-total_slots_used)/totReqSlot}")


    # max regeneration at which node:=
    max_regen_node = min(regeneration_resources, key=regeneration_resources.get)
    max_regen_time = regenerators - \
        regeneration_resources[max_regen_node]

    print(f"\033[35mMaximum number of regeneration occured at node: {max_regen_node} which is {max_regen_time} times.\033[0m")



    # total slots required:=
    print(f"\033[35mTotal slots required for processing {num_running_request} requests: {total_slots_used}\033[0m")


    # highest number of frequency slots used by
    def max_column_with_one(matrix):
        if not matrix:
            return -1  # If the matrix is empty, return -1 indicating no column with '1'
        
    # Initialize the maximum column number
        
        # Iterate through each column
        for col in range(len(matrix[0]) - 1, -1, -1):
            # Check if there is at least one '1' in the current column
            for row1 in range(len(matrix)):
                if matrix[row1][col] == 1:
                    return row1,col+1  # Return the column number if '1' is found
        return -1
    slotsMatrix = list(slotsLink.values())
    link,slots=max_column_with_one(slotsMatrix)
    # max_link, max_count = max(slotsLink.items(), key=lambda item: item[1].count(1))
    print(f"\033[35mHighest number of slots is used by link {list(slotsLink.keys())[link]} which is {slots}\033[0m")


    # total energy:=
    print(f"\033[35mTotal energy for processing 100 requests [1.BVT, 2. Optical Amplifier, 3.OXV]: {tot_energy} W\033[0m")

    # finding the variance
    reg_values = regeneration_resources.values()
    mean = sum(reg_values)/len(reg_values)
    squared_diff_sum = sum((num - mean) ** 2 for num in reg_values)
    variance = squared_diff_sum / len(reg_values)

    print(f"\033[35mVariance of regeneration of every node: {variance}\033[0m")

    print("With xBlocking Prob:----")
    print("Max Reg: ",max_regen_time*blocking_prob)
    print("Total Slots Used: ",total_slots_used*blocking_prob)
    print("Max index of slots: ",slots*blocking_prob)
    print("Total energy: ",tot_energy*blocking_prob)
    print("Variance : ",variance*blocking_prob)

    # print("Regeneration Upper Limit : ",max_regeneration)
    # print("Spectrum Efficiency :: (total frequency slot used / total number of request served) = ", total_slots_used/num_running_request)

if __name__ == "__main__":
    import sys
    request_path = sys.argv[1]
    num_regenerators = int(sys.argv[2])
    num_slots = int(sys.argv[3])
    tot_req_slot = int(sys.argv[4])
    main(request_path,num_regenerators,num_slots,tot_req_slot)