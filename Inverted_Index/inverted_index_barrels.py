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

#class for inverted index barrel generation
class InvertedIndex:
    # constructor
    def __init__(self):
        #number of barrels for inverted index
        self.number_of_inverted_index_barrels = 3000

        #list for storing the file path for each barrel
        self.inverted_index_file_paths = []

        #list for storing the data to be stored in each barrel
        self.inverted_indices = []

        #loop to store the file paths in the list
        for i in range(1, self.number_of_inverted_index_barrels + 1):
            self.inverted_index_file_paths.append(
                f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{i}.json')
        
        #loop to store the data of each barrel in a list corresponding to the correct index
        for path in self.inverted_index_file_paths:
            self.inverted_indices.append(self.load_inverted_index(path))

    #function for saving each barrel data in the corresponding barrel file
    def save_inverted_index_file(self, index, path):
        # Write inverted index to a JSON file
        with open(path, 'w') as json_file:
            json.dump(index, json_file)

    #function that calls each barrel file one by one and then saves them
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

                #converting the word id into int
                int_word_id = int(word_id)

                #converting word id back to string
                word_id = str(word_id)

                #getting the frequency
                frequency = word.get("fr")

                #getting the position
                positions = word.get("ps")

                #formula for deciding the barrel in which the word data will be stored
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


'''main function to load the forward index and then generating the inverted index'''
                        
#initializing the object for the inverted index class
inverted_index_generation = InvertedIndex()

#path where forward index files are stored
json_forward_index_dir = "./Forward_Index/Forward_index_files"
json_foward_index_files = [file for file in os.listdir(json_forward_index_dir) if file.endswith(".json")]

'''
loading all the forward index barrels one by one
and then generate inverted index for each forward index
barrel and then close the forward index barrel, then 
open the next forward index barrel
'''
for file_path in json_foward_index_files:
    forward_index = load_forward_index(
        os.path.join(json_forward_index_dir, file_path))
    inverted_index_generation.create_inverted_index(forward_index)


#finally saving all the inverted index barrels into the corresponding files
inverted_index_generation.save_all_inverted_index_files()
