import os
import json
# Directory containing JSON files
json_dir = "Inverted_Index/Inverted_index_files/inverted_index_barrel_5.json" 

# with open(json_dir, 'r') as f:
#     data = json.load(f)
#     print(len(data))
count = 0
# Get all JSON files in the directory
# print(len(json_files))
# Process each JSON file
    # Load data from JSON file
with open(json_dir, "r") as f:
    data = json.load(f)
    for w in data['word_ID']:
        count+=1
    # print(len(data))

print(count)    