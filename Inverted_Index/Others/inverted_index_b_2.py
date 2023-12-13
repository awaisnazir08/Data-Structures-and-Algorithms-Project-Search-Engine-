import json
import os

# function to load the forward index file
def load_forward_index(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("forward_index", [])
    except FileNotFoundError:
        print("No file for forward index exists..!!")

def load_lexicon():
    try:
        with open("./Forward_Index/Lexicon.json", 'r') as file:
            lexicon_data = json.load(file)
            if lexicon_data:
                max_word_id = max(lexicon_data.values())
                return max_word_id
            else:
                print("The lexicon file is empty!")
                return 0
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading lexicon file!")
        return 0

class InvertedIndex:
    # constructor
    def __init__(self):
        self.word_id_limit = 3000
        self.number_of_inverted_index_barrels = load_lexicon() // self.word_id_limit
        self.inverted_index_file_paths = []
        self.inverted_indices = []
        for i in range(1, self.number_of_inverted_index_barrels + 2):
            self.inverted_index_file_paths.append(f'Inverted_Index/Inverted_index_files2/inverted_index_barrel_{i}.json')
        for path in self.inverted_index_file_paths:
            self.inverted_indices.append(self.load_inverted_index(path))

    def save_inverted_index_file(self, index, path):
        # write inverted index to a JSON file
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
        barrel = 0
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
                check_duplication = (int_word_id ) // self.word_id_limit  # Adjust for starting from 1
                if word_id is not None:
                    # if the inverted index file is empty, initialize it with a key named word_ID
                    if "word_ID" not in self.inverted_indices[barrel]:
                        self.inverted_indices[barrel]["word_ID"] = {}
                    # if word is already not present in the inverted index, then create its key
                    if word_id not in self.inverted_indices[check_duplication]["word_ID"]:
                        self.inverted_indices[barrel]["word_ID"][word_id] = {}
                        # if a document id for a given word is already present, don't duplicate. else add the details for word in a document in a dictionary
                        if doc_id not in self.inverted_indices[barrel]["word_ID"][word_id]:
                            word_info = {
                                "fr": frequency,
                                "ps": positions
                            }
                            # add the details of the word for that document in the inverted index of the word
                            self.inverted_indices[barrel]["word_ID"][word_id][doc_id] = word_info

                        # Check if the length exceeds the limit, and if yes, save the file and reset the inverted index
                        if len(self.inverted_indices[barrel]["word_ID"]) >= self.word_id_limit:
                            self.save_inverted_index_file(self.inverted_indices[barrel], self.inverted_index_file_paths[barrel])
                            barrel += 1
                            self.inverted_indices[barrel] = {"word_ID": {}}

# main function to load the forward index and then generating the inverted index
inverted_index_generation = InvertedIndex()
json_forward_index_dir = "./Forward_Index/Forward_index_files2/forward_index.json"
forward_index = load_forward_index(json_forward_index_dir)
inverted_index_generation.create_inverted_index(forward_index)
inverted_index_generation.save_all_inverted_index_files()


# import json
# with open("Inverted_Index/Inverted_index_files/inverted_index_barrel_23.json" , 'r') as file:
#     data = json.load(file)
# print(len(data["word_ID"]))
