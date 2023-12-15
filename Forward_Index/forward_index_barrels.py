import json
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import hashlib


def calculate_mean_position(locations):
    if not locations:
        return None
    return sum(locations) // len(locations)
# class to create and manage a file that maps unique document ids to their unique urls
# the file is sorted according to the document ids
class Docid_Url_Mapping:
    # constructor
    def __init__(self):
        self.document_index_path = "Forward_Index/document_index.json"
        self.mappings = self.load_document_index()

    # add a new url with a unique document id into the file
    def add_to_document_index(self, doc_id, url):
        # check to see if a url is already present, it will not add it again
        if str(doc_id) not in self.mappings:
            self.mappings[doc_id] = url
            print(
                f"Document id: {doc_id} and corresponding url: {url} added in the document index")
        else:
            print("Already exists..!!")

    # if a file is already created and program is run again, the file wont be created again
    # instead, it will just be loaded
    def load_document_index(self):
        try:
            # Open the file in append mode
            with open(self.document_index_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # save the new updated file data into the file
    def save_document_index(self):
        with open(self.document_index_path, 'w') as file:
            json.dump(self.mappings, file)

# class to create and manage a file that maps document ids to the dates when they were published
# the file is sorted according to the document ids


class Docid_Date_Mapping:
    # constructor
    def __init__(self):
        self.docId_date_file_path = "Forward_Index/docId_date_mapping.json"
        self.mappings = self.load_docId_date_file()

    # adding new unique document id and its corresponding date in the file
    def add_to_docId_date_file(self, doc_id, date):
        if str(doc_id) not in self.mappings:
            self.mappings[doc_id] = date
            print(
                f"Document id: {doc_id} and corresponding date: {date} added in the document index")
        else:
            print("Already exists..!!")

    # if file already exists, it will simply be re-loaded for addition
    # if file doesn't exist, it will be created
    def load_docId_date_file(self):
        try:
            # Open the file in append mode
            with open(self.docId_date_file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # updated data saved into the file
    def save_docId_date_file(self):
        with open(self.docId_date_file_path, 'w') as file:
            json.dump(self.mappings, file)

# this class creates and manages a dictionary that stores all the unique words and assigns them
# new unique word_id in sorted order


class Lexicon:
    # constructor
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
                    # Update current ID
                    self.current_id = max(existing_data.values()) + 1
        except FileNotFoundError:
            pass

    # gets a word, checks if it doesn't exist, then assigns a new unique word id to the word and stores it
    # if the word exists, it will not be stored again
    def get_word_id(self, word):
        if word in self.word_to_id:
            return self.word_to_id[word]
        else:
            self.word_to_id[word] = self.current_id
            self.current_id += 1
            return self.word_to_id[word]

    # Write the updated word-to-ID mappings to new.json
    # the file is sorted according to the word ids in ascending order
    def save_lexicon_file(self):
        with open(self.lexicon_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.word_to_id, file)

# this class implements the checksum functionality in the forward index
# the checksum file is created to make sure that no duplicate articles/urls are stored in the forward index


class URLResolver:
    # constructor
    def __init__(self):
        self.checksums_file_path = 'Forward_Index/checksums.json'
        self.url_checksums = self.load_checksums_file()

    # loads the checksum file data if exists, else creates a new file
    def load_checksums_file(self):
        try:
            with open(self.checksums_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # checks if a unique checksum for a url is already available
    def resolve_doc_id(self, url_checksum):
        if url_checksum in self.url_checksums:
            return self.url_checksums[url_checksum]
        else:
            return None
    # adds a new checksum for a new url corresponding to the document id in the checksum file

    def add_document(self, url_checksum, doc_id):
        self.url_checksums[url_checksum] = doc_id

    # sorts the checksum file according to the checksums, so we can implement binary search easily while finding a document id
    def sort_file_with_respect_to_checksums_and_save(self):
        sorted_data = dict(
            sorted(self.url_checksums.items(), key=lambda x: x[0]))
        with open(self.checksums_file_path, 'w') as file:
            json.dump(sorted_data, file)

# creates and manages the forward index file


class Forward_Index:
    # constructor
    def __init__(self):
        self.number_of_barrels = 2000
        self.forward_index_paths = []
        self.forward_indices = []
        for i in range(1, self.number_of_barrels + 1):
            self.forward_index_paths.append(
                f'Forward_Index/Forward_index_files/forward_indexing_barrel_{i}.json')
        for path in self.forward_index_paths:
            self.forward_indices.append(self.load_forward_index(path))

    # if the forward index already exists, then loads it, else creates a dictionary for a new file
    def load_forward_index(self, path):
        try:
            # If forward index already exists
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            # Create a dictionary for storing the information
            return {"forward_index": []}

    # saves the forward index data into the file
    def save_forward_index_file(self, index, path):
        # Write the JSON structure to a file
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(index, json_file)

    # Add the entry to the forward_index dictionary
    # def add_to_forward_index(self, article_entry):
    #     self.forward_index["forward_index"].append(article_entry)

    def add_into_barrels(self, article_entry):
        doc_id = article_entry["d_id"]
        barrel = doc_id % self.number_of_barrels
        self.forward_indices[barrel]["forward_index"].append(article_entry)

    def save_all_forward_index_files(self):
        for index, path in zip(self.forward_indices, self.forward_index_paths):
            self.save_forward_index_file(index, path)


# setting up the english stop words from the NLTK
stop_words = set(stopwords.words('english'))

# object for the lemmatizer class
lemmatizer = WordNetLemmatizer()

# initializing the constructor for the Forward index clas
forwardIndex = Forward_Index()


# initializing the constructor for the Lexicon class
lex = Lexicon()

# initializing the constructor for the Doc id and url mapping class
docid_url_mapping = Docid_Url_Mapping()

# initializing the constructor for the Doc id and date mapping class
docid_date_mapping = Docid_Date_Mapping()

# Initializing the constructor for the URLResolver class
url_resolver = URLResolver()

# Directory containing JSON files of the dataset
json_dir = "./nela-gt-2022/newsdata"

# getiing all JSON files in the directory using the os module
json_files = [file for file in os.listdir(json_dir) if file.endswith(".json")]

# Load data from each JSON file one by one
for json_file in json_files:
    with open(os.path.join(json_dir, json_file), "r") as f:
        data = json.load(f)
        for article in data:
            url = article.get('url')
            if url.endswith('/'):
                # If yes, remove the trailing '/'
                url = url.rstrip('/')

            # implementing the blake 2s hash function on the url to generate a unique checksum for each url
            url_checksum = hashlib.blake2s(url.encode()).hexdigest()

            # checking if the url already exists
            doc_id = url_resolver.resolve_doc_id(url_checksum)

            if doc_id is not None:
                print(f"Article with URL '{url}' already has docID {doc_id}")
            else:
                # Assign a new docID
                doc_id = len(url_resolver.url_checksums) + 1
                url_resolver.add_document(url_checksum, doc_id)
                print(
                    f"Assigned new docID {doc_id} for article with URL '{url}'")

                # extracting information from the dataset articles
                content = article.get('content')
                title = article.get('title')
                date = article.get('date')

                # merging the title with the content
                title_and_content_merged = f"{title} {content}"

                # tokenizing the combined words
                words_tokenized = word_tokenize(title_and_content_merged)

                # Remove special characters, dots, etc.
                words_tokenized = [
                    word for word in words_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

                # Convert to lowercase
                words_tokenized = [word.lower() for word in words_tokenized]

                # Remove stop words
                clean_words = [
                    word for word in words_tokenized if word not in stop_words]

                # Lemmatization
                clean_words = [lemmatizer.lemmatize(
                    word) for word in clean_words]

                # Calculate word frequency and occurrence positions
                frequency_distribution = FreqDist(clean_words)

                # Initializing a new dictionary to store the positions for each word in the json file
                positions = {}

                title = title.lower()
                # Finding the position of each word
                for word in frequency_distribution.keys():
                    # positions[word] = []
                    locations = []
                    for pos, w in enumerate(clean_words):
                        if w == word:
                            # positions[word].append(pos)
                            locations.append(pos)
                    mean_position = calculate_mean_position(locations)
                    positions[word] = mean_position
                # Building the JSON object structure for every article
                article_entry = {
                    "d_id": doc_id,
                    "words": []
                }

                # adding unique doc_id and its url into the document index file
                docid_url_mapping.add_to_document_index(doc_id, url)

                # adding unique doc_id and its published in a separate file
                docid_date_mapping.add_to_docId_date_file(doc_id, date)

                # a json object for each word, its details, these will be stored in the list of words in the main json object
                for word in frequency_distribution.keys():
                    word_id = lex.get_word_id(word)
                    if word in title:
                        word_frequency = frequency_distribution[word] + 20
                    else:
                        word_frequency = frequency_distribution[word]
                    each_word_detail_in_an_article = {
                        "w_id": word_id,
                        "fr": word_frequency,
                        "ps": positions[word]
                    }
                    article_entry["words"].append(
                        each_word_detail_in_an_article)
                forwardIndex.add_into_barrels(article_entry)


# Save the updated URL checksums file
url_resolver.sort_file_with_respect_to_checksums_and_save()

# Write the JSON structure to forward index files
forwardIndex.save_all_forward_index_files()

# saving the lexicon dictionary
lex.save_lexicon_file()

# saving the document index file
docid_url_mapping.save_document_index()

# save the docId and date mapping file
docid_date_mapping.save_docId_date_file()

