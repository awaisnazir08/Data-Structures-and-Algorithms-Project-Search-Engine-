import os
import json
# Directory containing JSON files
json_dir = "./nela-gt-2022/newsdata"  # Replace with your actual path

count = 0
# Get all JSON files in the directory
json_files = [file for file in os.listdir(json_dir) if file.endswith(".json")]
print(len(json_files))
# Process each JSON file
for json_file in json_files:
    # Load data from JSON file
    with open(os.path.join(json_dir, json_file), "r") as f:
        data = json.load(f)
        count+=len(data)

print(count)