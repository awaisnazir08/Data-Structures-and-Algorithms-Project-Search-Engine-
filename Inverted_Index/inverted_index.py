import json
from collections import defaultdict

def save_inverted_index_file(inverted_index):
    # Write inverted index to a JSON file
    with open('Inverted_Index/inverted_index.json', 'w') as json_file:
        json.dump(inverted_index, json_file, indent=4)

def load_forward_index():
    forward_index_path = './Forward_Index/forward_indexing.json'
    try:
        with open(forward_index_path, 'r') as f:
            data = json.load(f)
            return data.get("forward_index", [])
    except FileNotFoundError:
        print("No file for forward index exists..!!")

def load_inverted_index():
    file_path = "Inverted_Index/inverted_index.json"
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"word_ID": {}}

def create_inverted_index(forward_index):
    inverted_index = load_inverted_index()
    for doc in forward_index:
        doc_id = doc["doc_id"]
        words = doc.get("words", [])
        doc_id = str(doc_id)
        for word in words:
            word_id = word.get("word")
            word_id = str(word_id)
            frequency = word.get("frequency")
            positions = word.get("positions")
            
            if word_id is not None:
                if "word_ID" not in inverted_index:
                    inverted_index["word_ID"] = {}
                if word_id not in inverted_index["word_ID"]:
                    inverted_index["word_ID"][word_id] = {}
                if doc_id not in inverted_index["word_ID"][word_id]:
                    word_info = {
                        "frequency": frequency,
                        "positions": positions
                    }

                    inverted_index["word_ID"][word_id][doc_id] = word_info

    # Remove duplicate word IDs
    # inverted_index = {k: v for k, v in inverted_index.items() if len(v) == len(set(v))}

    save_inverted_index_file(inverted_index)

    print("Inverted index generated and saved as 'inverted_index.json'")

forward_index = load_forward_index()
create_inverted_index(forward_index)
