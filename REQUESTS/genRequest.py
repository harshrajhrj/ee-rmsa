import random
# Aim:- Generate requests in separate files in following format
# <s, d1, d2, ..., dn, D> where n = 4

# Given(or input)

# Category input
# LSD - Low spectrum demand(40 Gbps, x = 1)
# MSD - Medium spectrum demand(80 Gbps, x = 2)
# HSD - High spectrum demand(120 Gbps, x = 3)
# VSD - Variable spectrum demand(40 - 160 Gbps, x = 1,2,3,4)

# No. of requests = 50x where x = 1,2,3,4,5,6
# No. of nodes = variable

# In random function,
# - Demand(in Gbps) = 40x where x = 1,2,3,4
# 	LSD, x = 1
# 	MSD, x = 2
# 	HSD, x = 3
# 	VSD, x = 1,2,3,4(use random function to generate)
# - Unique source <destinations> generation using random function on nodes

nodes = [24, 11, 14]
req_no = [50 * req for req in [1, 2, 3, 4, 5, 6]]

for node in nodes:
    for demand_type in ["LSD", "MSD", "HSD", "VSD"]:
        for req in req_no:
            req_file_name = f"{req}_{demand_type}_{node}.txt"
            with open("./REQUESTS/"+req_file_name, 'w', encoding='utf-8') as file:
                if demand_type == "LSD":
                    demand = 40
                elif demand_type == "MSD":
                    demand = 80
                elif demand_type == "HSD":
                    demand = 120
                
                list_of_nodes = set(range(1, node))
                for i in range(req):
                    
            
                    source = random.randint(1, node)
                    destination = random.sample(list_of_nodes - {source}, 5)
                    if demand_type == "VSD":
                        demand = random.randint(1, 4)*40
                    
                    file.write(str([source, destination, demand]) + '\n')

                