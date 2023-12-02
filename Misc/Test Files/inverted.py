import json
from collections import defaultdict



def load_forward_index():
    # Specify the path to the forward index file
    forward_index_path = './Forward_Index/forward_indexing.json'
    # Read forward index data from the specified file path
    try:
        with open(forward_index_path, 'r') as f:
            data = json.load(f)
            return data.get("forward_index", [])
    except FileNotFoundError:
        print("No file for forward index exists..!!")



# Create inverted index from forward index data 
def create_inverted_index(forward_index):
    # Initialize inverted index list
    inverted_index = []
    word_doc_mapping = defaultdict(list)
    for doc in forward_index:
        doc_id = doc["doc_id"]
        # date = doc["date"]
        words = doc.get("words", [])
        for word in words:
            word_id = word.get("word")
            frequency = word.get("frequency")
            positions = word.get("positions")
            word_information = {
                "frequency":frequency,
                "positions": positions
            }
            if word_id is not None:
                word_id = int(word_id)  # Convert word ID to an integer
                word_doc_mapping[word_id].append(doc_id)

    # Convert the lists to sets to remove duplicate document IDs (if any)
    for word_id, docs in sorted(word_doc_mapping.items()):
        doc_ids = list(set(docs))
        word_entry = {"doc_ID": doc_ids}
        inverted_index.append({str(word_id): word_entry})

    save_inverted_index_file(inverted_index)

    print("Inverted index generated and saved as 'inverted_index.json'")



forward_index = load_forward_index()

