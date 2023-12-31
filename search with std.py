import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import heapq
import sys
import time
import statistics


def calculate_standard_deviation(data):
    """
    Calculate the population standard deviation of a given array.

    Parameters:
    - data (list): List of numerical values.

    Returns:
    - float: Population standard deviation of the input data.
    """
    try:
        population_std_deviation = statistics.pstdev(data)
        return population_std_deviation
    except statistics.StatisticsError as e:
        print(f"Error calculating population standard deviation: {e}")
        return None

def calculate_score(frequency, sd):
    # Combine frequency and standard deviation into a score
    score = frequency / (1 + sd)

    return score

#function that loads the lexicon dictionary
def load_Lexicon():
    file_path = "Forward_Index/Lexicon.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None  

def load_documentIndex():
    file_path = "Forward_Index/document_index.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

def load_document_date_file():
    file_path = "Forward_Index/docId_date_mapping.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

def load_inverted_index_barrel(path):
    try: 
        with open(path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

def get_document_ids(word_id, word_data_in_barrel):
    if str(word_id) in word_data_in_barrel["word_ID"]:
        word_data = word_data_in_barrel["word_ID"][str(word_id)]
        # document_ids = list(word_data.keys())
        return word_data
    else:
        return {}


#setting up the english stop words from the NLTK
stop_words = set(stopwords.words('english'))

#object for the lemmatizer class
lemmatizer = WordNetLemmatizer()


lexicon_dictionary = load_Lexicon()

document_urls = load_documentIndex()


loaded_inverted_indices = {}
query = input("Enter the query to search: ")

start_time = time.time()
#tokenizing the combined words
query_tokenized = word_tokenize(query)

#remove special characters, dots, etc.
query_tokenized = [word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

#convert to lowercase
query_tokenized = [word.lower() for word in query_tokenized]

#remove stop words
clean_query = [word for word in query_tokenized if word not in stop_words]

#lemmatization
clean_query = [lemmatizer.lemmatize(word) for word
                in clean_query]

# priority_queue = []
document_score = {}
for word in clean_query:
    try: 
        word_id = lexicon_dictionary[word]
    except:
        print(f'{word} is not present in any document!')
        continue
    # print(word_id)
    barrel_id = word_id % 3000
    # print(barrel_id + 1)

    #check if the inverted index for this barrel is already loaded
    if barrel_id in loaded_inverted_indices:
        word_data_in_barrel = loaded_inverted_indices[barrel_id]
    else:
        #load the inverted index for this barrel
        word_data_in_barrel = load_inverted_index_barrel(f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{barrel_id + 1}.json')
        loaded_inverted_indices[barrel_id] = word_data_in_barrel

    documents = get_document_ids(word_id, word_data_in_barrel)

    for document in documents.keys():
        if document not in document_score:
            document_score[document] = {"count": 1, "values": [documents[document]]}
        else:
            document_score[document]["count"] += 1
            document_score[document]["values"].append(documents[document])

if(len(document_score)== 0):
    print("The searched word is not present in any document!\nPlease search another word..!!")
    sys.exit()

max_count_document = max(document_score.items(), key=lambda x: x[1]["count"])
max_count = max_count_document[1]["count"]
print(max_count)

documents_shown = 0

while(documents_shown < 30 and max_count >=1):
    priority_queue = []
    for doc in document_score.items():
        if doc[1]["count"] == max_count:
            getting_frequencies = doc[1]['values']
            # print(getting_frequencies)
            frequency = 0
            positions = []
            for value in getting_frequencies:
                frequency += value['fr']
                positions.append(value['ps'])
            frequency /= len(getting_frequencies)
            standard_deviation = calculate_standard_deviation(positions)
            score = calculate_score(frequency, standard_deviation)
            heapq.heappush(priority_queue, (-score, doc[0]))
    # documents_shown += len(priority_queue)
    max_count -= 1
    for _ in range(len(priority_queue)):
        if priority_queue:
            if(documents_shown >= 30):
                break
            score, document_id = heapq.heappop(priority_queue)
            document_url = document_urls[document_id]
            print(document_id, " ", -score, " ", document_url)
            documents_shown += 1


end_time = time.time()

execution_time = end_time - start_time
print(f"Code took {execution_time:.6f} seconds to run.")
