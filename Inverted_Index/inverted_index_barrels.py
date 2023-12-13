import json
import os

# function to load the forward index file


def load_forward_index(file_path):
    # forward_index_file_paths = './Forward_Index/forward_indexing.json'
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("forward_index", [])
    except FileNotFoundError:
        print("No file for forward index exists..!!")


class InvertedIndex:
    # constructor
    def __init__(self):
        self.number_of_inverted_index_barrels = 2000
        self.inverted_index_file_paths = []
        self.inverted_indices = []
        for i in range(1, self.number_of_inverted_index_barrels + 1):
            self.inverted_index_file_paths.append(
                f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{i}.json')
        for path in self.inverted_index_file_paths:
            self.inverted_indices.append(self.load_inverted_index(path))

    def save_inverted_index_file(self, index, path):
        # Write inverted index to a JSON file
        with open(path, 'w') as json_file:
            json.dump(index, json_file, indent=4)

    def save_all_inverted_index_files(self):
        for index, path in zip(self.inverted_indices, self.inverted_index_file_paths):
            self.save_inverted_index_file(index, path)

    # function to load the inverted index file if already exists, else creates a dictionary for inverted index
    def load_inverted_index(self, path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"word_ID": {}}

    # this function creates the structure to be inserted into the inverted index file
    def create_inverted_index(self, forward_index):
        # iterating through each document in the forward index
        for doc in forward_index:
            # getting the document id and words associated with each document
            doc_id = doc["d_id"]
            words = doc.get("words", [])
            doc_id = str(doc_id)

            # getting the information for each word present in a particular document
            for word in words:
                word_id = word.get("w_id")
                int_word_id = int(word_id)
                word_id = str(word_id)
                frequency = word.get("fr")
                positions = word.get("ps")
                barrel = int_word_id % self.number_of_inverted_index_barrels
                if word_id is not None:
                    # if the inverted index file is empty, initialize it with a key named word_ID
                    if "word_ID" not in self.inverted_indices[barrel]:
                        self.inverted_indices[barrel]["word_ID"] = {}
                    # if word is already not present in the inverted index, then create its key
                    if word_id not in self.inverted_indices[barrel]["word_ID"]:
                        self.inverted_indices[barrel]["word_ID"][word_id] = {}
                    # if a document id for a given word is already present, don't duplicate. else add the details for word in a document in a dictionary
                    if doc_id not in self.inverted_indices[barrel]["word_ID"][word_id]:
                        word_info = {
                            "fr": frequency,
                            "ps": positions
                        }
                        # add the details of the word for that document in the inverted index of the word
                        self.inverted_indices[barrel]["word_ID"][word_id][doc_id] = word_info


# main function to load the forward index and then generating the inverted index
inverted_index_generation = InvertedIndex()
json_forward_index_dir = "./Forward_Index/Forward_index_files"
json_foward_index_files = [file for file in os.listdir(
    json_forward_index_dir) if file.endswith(".json")]
for file_path in json_foward_index_files:
    forward_index = load_forward_index(
        os.path.join(json_forward_index_dir, file_path))
    inverted_index_generation.create_inverted_index(forward_index)

inverted_index_generation.save_all_inverted_index_files()
