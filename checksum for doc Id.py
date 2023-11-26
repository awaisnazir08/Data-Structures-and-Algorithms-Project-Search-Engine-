import json
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import hashlib
import bisect

class Lexicon:
    def __init__(self):
        self.word_to_id = {}
        self.current_id = 1

        # Load existing data from Lexicon.json (if exists)
        try:
            with open('Lexicon.json', 'r') as file:
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

class URLResolver:
    def __init__(self, checksums_file_path):
        self.url_checksums = self.load_checksums_file(checksums_file_path)

    def load_checksums_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
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

    def save_checksums_to_file(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.url_checksums, file)

    def sort_file_with_respect_to_checksums(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        with open(file_path, 'w') as file:
            json.dump(dict(sorted_data), file)

# Set up NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Create a dictionary for storing the information
forward_index = {"forward_index": []}

# Directory containing JSON files
json_dir = "./nela-gt-2022/newsdata/21stcenturywire.json"

article_id = 0

# Initializing the constructor for the Lexicon class
lex = Lexicon()

# Initializing the constructor for the URLResolver class
url_resolver = URLResolver('checksums.json')

with open(json_dir, "r") as f:
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

        # Finding the position of each word
        for word in frequency_distribution.keys():
            positions[word] = []
            for pos, w in enumerate(clean_words):
                if w == word:
                    positions[word].append(pos)

        # Building the JSON object structure for every article
        article_entry = {
            "doc_id": doc_id,
            "url": url,
            "date": date,
            "words": []
        }
        # json object within a json object(inside list)
        # a json object for each word, its details, these will be stored in the list of words in the main json object
        for word in frequency_distribution.keys():
            word_id = lex.get_word_id(word)
            each_word_detail_in_an_article = {
                "word": word_id,
                "frequency": frequency_distribution[word],
                "positions": positions[word]
            }
            article_entry["words"].append(each_word_detail_in_an_article)

        # Add the entry to the forward_index dictionary
        forward_index["forward_index"].append(article_entry)
        article_id += 1

# Save the updated URL checksums file
url_resolver.save_checksums_to_file('checksums.json')
url_resolver.sort_file_with_respect_to_checksums('checksums.json')

# Write the JSON structure to a file
json_file_path = 'forward_indexing3.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(forward_index, json_file, indent=2)

# Write the updated word-to-ID mappings to new.json
with open('Lexicon.json', 'w') as file:
    json.dump(lex.word_to_id, file, indent=2)

