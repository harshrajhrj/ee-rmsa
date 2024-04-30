import ast

# Open the file and read its contents
with open('requests.txt', 'r',encoding='utf-8') as file:
    request_str = file.read().rstrip()

request_list_str=request_str.split('\n')

# Convert the string to a list using ast.literal_eval()
for one_request_str in request_list_str:
    new_request = ast.literal_eval(one_request_str)
    print(new_request,type(new_request))
# Print the resulting list

