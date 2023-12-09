import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

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



# class SearchEngine:
#     def __init__(self):



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

# Remove special characters, dots, etc.
query_tokenized = [word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

# Convert to lowercase
query_tokenized = [word.lower() for word in query_tokenized]

# Remove stop words
clean_query = [word for word in query_tokenized if word not in stop_words]

# Lemmatization
clean_query = [lemmatizer.lemmatize(word) for word in clean_query]

for word in clean_query:
    word_id = lexicon_dictionary[word]
    print(word_id)
    barrel_id = word_id % 100
    print(barrel_id + 1)

    # Check if the inverted index for this barrel is already loaded
    if barrel_id in loaded_inverted_indices:
        word_data_in_barrel = loaded_inverted_indices[barrel_id]
    else:
        # Load the inverted index for this barrel
        word_data_in_barrel = load_inverted_index_barrel(f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{barrel_id + 1}.json')
        loaded_inverted_indices[barrel_id] = word_data_in_barrel

    documents = get_document_ids(word_id, word_data_in_barrel)


    # Calculate scores based on frequencies and positions
    scores = {}
    for document_id, data in documents.items():
        frequency = data.get("fr", 0)
        positions = data.get("ps", [])

        # Avoid division by zero error
        position_score = sum(1 / pos for pos in positions if pos != 0) if positions else 0

        scores[document_id] = frequency * position_score

    # Sort documents by score in descending order
    sorted_documents = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True)[:30])

    for document_id in sorted_documents.keys():
        document_url = document_urls[document_id]
        print(document_id, " ", sorted_documents[document_id], " ", document_url)





    # sorted_documents_based_on_frequency = dict(sorted(documents.items(), key=lambda item: item[1]["fr"], reverse=True)[:30])

    # for document_id in sorted_documents_based_on_frequency.keys():
    #     document_url = document_urls[document_id]
    #     # print(document_url)

    #     # print(document_id)
    #     print(document_id," ", sorted_documents_based_on_frequency[document_id], " ", document_url)

