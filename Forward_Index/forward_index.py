import json
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import hashlib
# import bisect


class Docid_Url_Mapping:
    def __init__(self):
        self.document_index_path = "Forward_Index/document_index.json"
        self.mappings = self.load_document_index()

    def add_to_document_index(self, doc_id, url):
        if str(doc_id) not in self.mappings:
            self.mappings[doc_id] = url
            print(f"Document id: {doc_id} and corresponding url: {url} added in the document index")
        else:
            print("Already exists..!!")

    def load_document_index(self):
        try:
            # Open the file in append mode
            with open(self.document_index_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_document_index(self):
        with open(self.document_index_path, 'w') as file:
            json.dump(self.mappings, file, indent = 2)

class Docid_Date_Mapping:
    def __init__(self):
        self.docId_date_file_path = "Forward_Index/docId_date_mapping.json"
        self.mappings = self.load_docId_date_file()

    def add_to_docId_date_file(self, doc_id, date):
        if str(doc_id) not in self.mappings:
            self.mappings[doc_id] = date
            print(f"Document id: {doc_id} and corresponding date: {date} added in the document index")
        else:
            print("Already exists..!!")

    def load_docId_date_file(self):
        try:
            # Open the file in append mode
            with open(self.docId_date_file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_docId_date_file(self):
        with open(self.docId_date_file_path, 'w') as file:
            json.dump(self.mappings, file, indent = 2)

class Lexicon:
    def __init__(self):
        self.word_to_id = {}
        self.current_id = 1
        self.lexicon_file_path = 'Forward_Index/Lexicon.json'
        # Load existing data from Lexicon.json (if exists)
        try:
            with open(self.lexicon_file_path, 'r') as file:
                existing_data = json.load(file)
                if existing_data:
                    self.word_to_id = existing_data  # Load existing data
                    self.current_id = max(existing_data.values()) + 1  # Update current ID
        except FileNotFoundError:
            pass

    def get_word_id(self, word):
        if word in self.word_to_id:
            return self.word_to_id[word]
        else:
            self.word_to_id[word] = self.current_id
            self.current_id += 1
            return self.word_to_id[word]

    # Write the updated word-to-ID mappings to new.json
    def save_lexicon_file(self):
        with open(self.lexicon_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.word_to_id, file, indent=2)

class URLResolver:
    def __init__(self):
        self.checksums_file_path = 'Forward_Index/checksums.json'
        self.url_checksums = self.load_checksums_file()

    def load_checksums_file(self):
        try:
            with open(self.checksums_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def resolve_doc_id(self, url_checksum):
        if url_checksum in self.url_checksums:
            return self.url_checksums[url_checksum]
        else:
            return None

    def add_document(self, url_checksum, doc_id):
        self.url_checksums[url_checksum] = doc_id

    def sort_file_with_respect_to_checksums_and_save(self):
        sorted_data = dict(sorted(self.url_checksums.items(), key=lambda x: x[0]))
        with open(self.checksums_file_path, 'w') as file:
            json.dump(sorted_data, file)

class Forward_Index:
    def __init__(self):
        self.forward_index_path = 'Forward_Index/forward_indexing.json'
        self.forward_index = self.load_forward_index()

    def load_forward_index(self):
        try:
            #If forward index already exists
            with open(self.forward_index_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            # Create a dictionary for storing the information
            return {"forward_index": []}
        
    def save_forward_index_file(self):
    # Write the JSON structure to a file
        with open(self.forward_index_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.forward_index, json_file, indent=2)

    # Add the entry to the forward_index dictionary
    def add_to_forward_index(self, article_entry):
        self.forward_index["forward_index"].append(article_entry)


# Set up NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


forwardIndex = Forward_Index()


# Initializing the constructor for the Lexicon class
lex = Lexicon()
docid_url_mapping = Docid_Url_Mapping()
docid_date_mapping = Docid_Date_Mapping()

# Initializing the constructor for the URLResolver class
url_resolver = URLResolver()

# Directory containing JSON files
json_dir = "./nela-gt-2022/newsdata"

# Get all JSON files in the directory
json_files = [file for file in os.listdir(json_dir) if file.endswith(".json")]



for json_file in json_files:
    # Load data from JSON file
    with open(os.path.join(json_dir, json_file), "r") as f:
        data = json.load(f)
        for article in data:
            url = article.get('url')
            if url.endswith('/'):
            # If yes, remove the trailing '/'
                url = url.rstrip('/')

            url_checksum = hashlib.blake2s(url.encode()).hexdigest()
            doc_id = url_resolver.resolve_doc_id(url_checksum)

            if doc_id is not None:
                print(f"Article with URL '{url}' already has docID {doc_id}")
            else:
                # Assign a new docID
                doc_id = len(url_resolver.url_checksums) + 1
                url_resolver.add_document(url_checksum, doc_id)
                print(f"Assigned new docID {doc_id} for article with URL '{url}'")

                content = article.get('content')
                title = article.get('title')
                date = article.get('date')
                title_and_content_merged = f"{title} {content}"
                words_tokenized = word_tokenize(title_and_content_merged)

                # Remove special characters, dots, etc.
                words_tokenized = [word for word in words_tokenized if word.isalpha()]

                # Convert to lowercase
                words_tokenized = [word.lower() for word in words_tokenized]

                # Remove stop words
                clean_words = [word for word in words_tokenized if word not in stop_words]

                # Lemmatization
                clean_words = [lemmatizer.lemmatize(word) for word in clean_words]

                # Calculate word frequency and occurrence positions
                frequency_distribution = FreqDist(clean_words)

                # Initializing a new dictionary to store the positions for each word in the json file
                positions = {}

                title = title.lower()
                # Finding the position of each word
                for word in frequency_distribution.keys():
                    positions[word] = []
                    for pos, w in enumerate(clean_words):
                        if w == word:
                            positions[word].append(pos)

                # Building the JSON object structure for every article
                article_entry = {
                    "doc_id": doc_id,
                    "words": []
                }
                docid_url_mapping.add_to_document_index(doc_id, url)
                docid_date_mapping.add_to_docId_date_file(doc_id, date)
                # json object within a json object(inside list)
                # a json object for each word, its details, these will be stored in the list of words in the main json object
                for word in frequency_distribution.keys():
                    word_id = lex.get_word_id(word)
                    if word in title:
                        word_frequency = frequency_distribution[word] + 20
                    else:
                        word_frequency = frequency_distribution[word]
                    each_word_detail_in_an_article = {
                        "word": word_id,
                        "frequency": word_frequency,
                        "positions": positions[word]
                    }
                    article_entry["words"].append(each_word_detail_in_an_article)
                forwardIndex.add_to_forward_index(article_entry)


# Save the updated URL checksums file
url_resolver.sort_file_with_respect_to_checksums_and_save()

# Write the JSON structure to a file
forwardIndex.save_forward_index_file()

lex.save_lexicon_file()

docid_url_mapping.save_document_index()
docid_date_mapping.save_docId_date_file()

