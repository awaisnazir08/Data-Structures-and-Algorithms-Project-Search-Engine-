import json
from collections import defaultdict

def generate_inverted_index(forward_index_path):
    # Read forward index data from the specified file path
    with open(forward_index_path, 'r') as f:
        data = json.load(f)
        forward_index = data.get("forward_index", [])

    # Initialize inverted index list
    inverted_index = []

    # Create inverted index from forward index data
    word_doc_mapping = defaultdict(list)
    for doc in forward_index:
        doc_id = doc["doc_id"]
        words = doc.get("words", [])
        for word_info in words:
            word = word_info.get("word")
            if word is not None:
                word = int(word)  # Convert word ID to an integer
                word_doc_mapping[word].append(doc_id)

    # Convert the lists to sets to remove duplicate document IDs (if any)
    for word, docs in sorted(word_doc_mapping.items()):
        doc_ids = list(set(docs))
        word_entry = {"doc_ID": doc_ids}
        inverted_index.append({str(word): word_entry})

    # Write inverted index to a JSON file
    with open('Inverted_Index/inverted_index.json', 'w') as json_file:
        json.dump({"word_ID": inverted_index}, json_file, indent=4)

    print("Inverted index generated and saved as 'inverted_index.json'")

# Specify the path to the forward index file
forward_index_file_path = './Forward_Index/forward_indexing.json'

# Generate the inverted index
generate_inverted_index(forward_index_file_path)
