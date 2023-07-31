# 


# communication_history = "{\"longitude\": \"3.3370874\", \"latitude\": \"6.5919131\", \"timestamp\": \"2023-07-30T23:39:38.782082+00:00\"}{\"longitude\": \"3.3371672\", \"latitude\": \"6.5915762\", \"timestamp\": \"2023-07-30T23:39:40.651739+00:00\"}{\"longitude\": \"3.3371672\", \"latitude\": \"6.5915762\", \"timestamp\": \"2023-07-30T23:39:40.656671+00:00\"}"
# communication_list = communication_history.split("}{")

# d = []
# for i, data in enumerate(communication_list):
    
#     if i == 0:
#         communication_list[i] = data+'}'
        
#     elif i+1 == len(communication_list):
#         communication_list[i] = '{'+data
#     else:
#         communication_list[i] = '{'+data+'}'

#     d.append(eval(communication_list[i]))
    
# print(d)
# print(communication_list)

import json

communication_history = "{\"longitude\": \"3.3370874\", \"latitude\": \"6.5919131\", \"timestamp\": \"2023-07-30T23:39:38.782082+00:00\"}{\"longitude\": \"3.3371672\", \"latitude\": \"6.5915762\", \"timestamp\": \"2023-07-30T23:39:40.651739+00:00\"}{\"longitude\": \"3.3371672\", \"latitude\": \"6.5915762\", \"timestamp\": \"2023-07-30T23:39:40.656671+00:00\"}"

# Add commas between individual JSON objects to form a valid JSON array.
communication_history = "[" + communication_history.replace("}{", "},{") + "]"

# Parse the JSON array into a list of dictionaries.
d = json.loads(communication_history)

print(d)

