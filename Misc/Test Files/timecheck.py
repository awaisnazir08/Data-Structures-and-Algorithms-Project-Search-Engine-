import json
import time

start_time = time.time()

with open("Inverted_Index/Inverted_index_files/inverted_index_barrel_21.json", "r") as file:
    data = json.load(file)
    print(len(data["word_ID"]))
end_time = time.time()

execution_time = end_time - start_time
print(f"Code took {execution_time:.6f} seconds to run.")
