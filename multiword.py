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
# Initialize a set to store the common document IDs
common_document_ids = set()

# Iterate over each word in the cleaned query
for word in clean_query:
    word_id = lexicon_dictionary[word]
    barrel_id = word_id % 100

    # Check if the inverted index for this barrel is already loaded
    if barrel_id in loaded_inverted_indices:
        word_data_in_barrel = loaded_inverted_indices[barrel_id]
    else:
        # Load the inverted index for this barrel
        word_data_in_barrel = load_inverted_index_barrel(f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{barrel_id + 1}.json')
        loaded_inverted_indices[barrel_id] = word_data_in_barrel

    # Get document IDs for the current word
    document_ids = set(get_document_ids(word_id, word_data_in_barrel).keys())

    # If common_document_ids is empty, initialize it with the document IDs from the first word
    if not common_document_ids:
        common_document_ids.update(document_ids)
    else:
        # Intersect the current document_ids with common_document_ids
        common_document_ids.intersection_update(document_ids)

# Now, common_document_ids contains the common document IDs across all words in the query

# Display the common document IDs
print("Common Document IDs:", common_document_ids)

# Optionally, you can print more details about the common documents
for document_id in common_document_ids:
    document_url = document_urls[document_id]
    print(f"Document ID: {document_id}, URL: {document_url}")
    # for document_id in sorted_documents_based_on_frequency.keys():
    #     document_url = document_urls[document_id]
    #     # print(document_url)

    #     # print(document_id)
    #     print(document_id," ", sorted_documents_based_on_frequency[document_id], " ", document_url)
