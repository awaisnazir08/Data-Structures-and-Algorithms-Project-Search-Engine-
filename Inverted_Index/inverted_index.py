import json
from collections import defaultdict

def save_inverted_index_file(inverted_index):
    # Write inverted index to a JSON file
    with open('Inverted_Index/inverted_index.json', 'w') as json_file:
        json.dump(inverted_index, json_file, indent=4)

#function to load the forward index file
def load_forward_index():
    forward_index_path = './Forward_Index/forward_indexing.json'
    try:
        with open(forward_index_path, 'r') as f:
            data = json.load(f)
            return data.get("forward_index", [])
    except FileNotFoundError:
        print("No file for forward index exists..!!")

#function to load the inverted index file if already exists, else creates a dictionary for inverted index
def load_inverted_index():
    file_path = "Inverted_Index/inverted_index.json"
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"word_ID": {}}

#this function creates the structure to be inserted into the inverted index file
def create_inverted_index(forward_index):
    inverted_index = load_inverted_index()

    #iterating through each document in the forward index
    for doc in forward_index:
        #getting the document id and words associated with each document
        doc_id = doc["doc_id"]
        words = doc.get("words", [])
        doc_id = str(doc_id)

        #getting the information for each word present in a particular document
        for word in words:
            word_id = word.get("word")
            word_id = str(word_id)
            frequency = word.get("frequency")
            positions = word.get("positions")
            
            if word_id is not None:
                #if the inverted index file is empty, initialize it with a key named word_ID
                if "word_ID" not in inverted_index:
                    inverted_index["word_ID"] = {}
                #if word is already not present in the inverted index, then create its key
                if word_id not in inverted_index["word_ID"]:
                    inverted_index["word_ID"][word_id] = {}
                #if a document id for a given word is already present, don't duplicate. else add the details for word in a document in a dictionary
                if doc_id not in inverted_index["word_ID"][word_id]:
                    word_info = {
                        "frequency": frequency,
                        "positions": positions
                    }

                    #add the details of the word for that document in the inverted index of the word
                    inverted_index["word_ID"][word_id][doc_id] = word_info


    #save the updated inverted index dictionary in a json file
    save_inverted_index_file(inverted_index)

    print("Inverted index generated and saved as 'inverted_index.json'")

#main function to load the forward index and then generating the inverted index
forward_index = load_forward_index()
create_inverted_index(forward_index)
