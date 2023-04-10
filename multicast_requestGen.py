# Open the file containing the adjacency matrix

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

# reading request from request.txt file

with open('requests.txt', 'r', encoding='utf-8') as file:
    request_str = file.read().rstrip()

request_list_str = request_str.split('\n')

# Convert the string to a list using ast.literal_eval()
for one_request_str in request_list_str:
    new_request = ast.literal_eval(one_request_str)
# print(one_request_str)