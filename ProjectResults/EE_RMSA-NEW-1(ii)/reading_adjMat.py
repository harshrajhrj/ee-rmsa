# Open the file containing the adjacency matrix
with open('adjmat_USA.txt', 'r',encoding='utf-8') as f:
    contents = f.read()

rows = contents.split('\n')

adj_matrix = []

# Loop through each row of the matrix
for row in rows:
    # processing the data
    row=row.rstrip()
    values = row.split(' ')

    # Convert the values to integers
    values = [int(val) for val in values]

    # Add the row to the adjacency matrix
    adj_matrix.append(values)

print("Adj matrix is ready......")


# Iterate over each row of the matrix
for row in adj_matrix:
    # Get the length of the row (i.e., the number of elements in the row)
    num_elements = len(row)
    
    # Print the number of elements in the row
    print(f"Number of elements in row {adj_matrix.index(row)+1}: {num_elements}")

