# Generating 100 such sample request:  [1,[2,3,4],40X] in requests.txt file

import random
# f = open("request.txt","w",encoding='utf-8')


request = []
list_of_nodes = set(range(1, 25))

with open("requests.txt", "w", encoding='utf-8') as f:

    for i in range(100):
        # Generate a list of 5 random integers between 1 and 24 (inclusive)
        source = random.randint(1, 24)
        destination = random.sample(list_of_nodes - {source}, 5)
        bwd = random.randint(1, 4)*40
        f.write(str([source, destination, bwd]) + '\n')
