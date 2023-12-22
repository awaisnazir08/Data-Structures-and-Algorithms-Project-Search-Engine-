import os
import json

def count_objects(folder_path):
    total_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    num_objects = len(data)
                    total_count += num_objects



                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")
                    continue
    print(f"the total count is {total_count}")

# Replace 'your_folder_path' with the path to your folder containing JSON files
folder_path = 'nela-gt-2022/newsdata/new'

count_objects(folder_path)
