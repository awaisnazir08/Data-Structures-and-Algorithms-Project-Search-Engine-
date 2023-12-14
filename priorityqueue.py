import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import heapq  # Import heapq module for priority queue

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

inverted_index_file_paths = []
for i in range(1, 101):
    inverted_index_file_paths.append(f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{i}.json')

lexicon_dictionary = load_Lexicon()

document_urls = load_documentIndex()


loaded_inverted_indices = {}
query = input("Enter the query to search: ")

#tokenizing the combined words
query_tokenized = word_tokenize(query)

#remove special characters, dots, etc.
query_tokenized = [word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

#convert to lowercase
query_tokenized = [word.lower() for word in query_tokenized]

#remove stop words
clean_query = [word for word in query_tokenized if word not in stop_words]

#lemmatization
clean_query = [lemmatizer.lemmatize(word) for word in clean_query]

priority_queue = []
document_score = {}
for word in clean_query:
    word_id = lexicon_dictionary[word]
    print(word_id)
    barrel_id = word_id % 2000
    print(barrel_id + 1)

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

max_count_document = max(document_score.items(), key=lambda x: x[1]["count"])
max_count = max_count_document[1]["count"]
print(max_count)
# document_score_items = list(document_score.items())
# document_score_items.sort(key=lambda x: x[1]['count'], reverse=True)
sorted_items = sorted(document_score.items(), key=lambda x: x[1]['count'], reverse=False)

for doc in sorted_items:
    # print(doc[1]["count"])
    if doc[1]["count"] == max_count:
        getting_frequencies = doc[1]['values']
        # print(getting_frequencies)
        frequency = 0
        for value in getting_frequencies:
            frequency += value['fr']
        # frequency /= len(getting_frequencies)
        print(frequency)
        heapq.heappush(priority_queue, (-frequency, doc[0]))  # Use -fr for max heap
for _ in range(30):
    if priority_queue:
        frequency, document_id = heapq.heappop(priority_queue)
        document_url = document_urls[document_id]
        print(document_id, " ", -frequency, " ", document_url)
# print(sorted_items[0]['count'])
# for element in sorted_items:
#     print(element)
# #use a priority queue to maintain the top documents based on frequency
# for document_id, data in documents.items():
#     frequency = data["fr"]
#     heapq.heappush(priority_queue, (-frequency, document_id))  # Use -fr for max heap

# #extract and print the top documents from the priority queue
# for _ in range(30):
#     if priority_queue:
#         frequency, document_id = heapq.heappop(priority_queue)
#         document_url = document_urls[document_id]
#         print(document_id, " ", -frequency, " ", document_url)


# def score(frequency, sd):
#     # Calculate frequency


#     # Combine frequency and standard deviation into a score
#     score = frequency / (1 + sd)

#     return score

# # s = score(7, 5)
# print(score(7, 15))
# print(score(10, 2))
# print(score(6, 0.2))
# print(score(20, 20))