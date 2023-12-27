from nltk.probability import FreqDist
import hashlib
import json
from flask import Flask, request, jsonify
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from flask_cors import CORS
import time
import heapq
import os


app = Flask(__name__)
CORS(app)


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


def get_documents(word_id, word_data_in_barrel):
    if str(word_id) in word_data_in_barrel["word_ID"]:
        word_data = word_data_in_barrel["word_ID"][str(word_id)]
        return word_data
    else:
        return {}


stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
lexicon_dictionary = load_Lexicon()
document_urls = load_documentIndex()
loaded_inverted_indices = {}


@app.route("/search", methods=["POST"])
def search_query():
    data = request.get_json()
    query = data.get("query")

    start_time = time.time()
    query_tokenized = word_tokenize(query)
    query_tokenized = [
        word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)
    ]
    query_tokenized = [word.lower() for word in query_tokenized]
    clean_query = [word for word in query_tokenized if word not in stop_words]
    clean_query = [lemmatizer.lemmatize(word) for word in clean_query]
    document_score = {}

    for word in clean_query:
        try:
            word_id = lexicon_dictionary[word]
        except:
            print(f"{word} is not present in any document!")
            continue

        barrel_id = word_id % 3000

        if barrel_id in loaded_inverted_indices:
            word_data_in_barrel = loaded_inverted_indices[barrel_id]
        else:
            word_data_in_barrel = load_inverted_index_barrel(
                f"Inverted_Index/Inverted_index_files/inverted_index_barrel_{barrel_id + 1}.json"
            )
            loaded_inverted_indices[barrel_id] = word_data_in_barrel

        documents = get_documents(word_id, word_data_in_barrel)

        for document in documents.keys():
            if document not in document_score:
                document_score[document] = {"count": 1, "values": [documents[document]]}
            else:
                document_score[document]["count"] += 1
                document_score[document]["values"].append(documents[document])

    if len(document_score) == 0:
        response = {
            "message": "The searched query is not present in any document!",
            "details": "Please search for other words..!!",
        }
        return jsonify(response), 404

    max_count_document = max(document_score.items(), key=lambda x: x[1]["count"])
    max_count = max_count_document[1]["count"]
    documents_shown = 0
    search_results = []

    while documents_shown < 30 and max_count >= 1:
        priority_queue = []

        for doc in document_score.items():
            if doc[1]["count"] == max_count:
                getting_frequencies = doc[1]["values"]
                frequency = 0

                for value in getting_frequencies:
                    frequency += value["fr"]

                heapq.heappush(priority_queue, (-frequency, doc[0]))

        max_count -= 1

        for _ in range(len(priority_queue)):
            if priority_queue:
                if documents_shown >= 30:
                    break
                frequency, document_id = heapq.heappop(priority_queue)
                document_url = document_urls[document_id]
                search_results.append(
                    {
                        "document_id": document_id,
                        "frequency": -frequency,
                        "document_url": document_url,
                    }
                )
                documents_shown += 1

    end_time = time.time()
    execution_time = end_time - start_time

    response = {
        "message": "Search results",
        "query": query,
        "documents": search_results,
        "execution_time": execution_time,
    }

    return jsonify(response), 200


########################################
########################################
########################################
# Implementing the add functionality here
########################################
########################################
########################################


def calculate_mean_position(locations):
    if not locations:
        return None
    return sum(locations) // len(locations)


class Docid_Url_Mapping:
    def __init__(self):
        self.document_index_path = "Forward_Index/document_index.json"
        self.mappings = self.load_document_index()

    def add_to_document_index(self, doc_id, url):
        if str(doc_id) not in self.mappings:
            self.mappings[doc_id] = url
            print(
                f"Document id: {doc_id} and corresponding url: {url} added in the document index"
            )
        else:
            print("Already exists..!!")

    def load_document_index(self):
        try:
            # Open the file in append mode
            with open(self.document_index_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_document_index(self):
        with open(self.document_index_path, "w") as file:
            json.dump(self.mappings, file)


class Docid_Date_Mapping:
    # constructor
    def __init__(self):
        self.docId_date_file_path = "Forward_Index/docId_date_mapping.json"
        self.mappings = self.load_docId_date_file()

    def add_to_docId_date_file(self, doc_id, date):
        if str(doc_id) not in self.mappings:
            self.mappings[doc_id] = date
            print(
                f"Document id: {doc_id} and corresponding date: {date} added in the document index"
            )
        else:
            print("Already exists..!!")

    def load_docId_date_file(self):
        try:
            # Open the file in append mode
            with open(self.docId_date_file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_docId_date_file(self):
        with open(self.docId_date_file_path, "w") as file:
            json.dump(self.mappings, file)


class Lexicon:
    def __init__(self):
        self.word_to_id = {}
        self.current_id = 1
        self.lexicon_file_path = "Forward_Index/Lexicon.json"
        try:
            with open(self.lexicon_file_path, "r") as file:
                existing_data = json.load(file)
                if existing_data:
                    self.word_to_id = existing_data  # Load existing data
                    # Update current ID
                    self.current_id = max(existing_data.values()) + 1
        except FileNotFoundError:
            pass

    def get_word_id(self, word):
        if word in self.word_to_id:
            return self.word_to_id[word]
        else:
            self.word_to_id[word] = self.current_id
            self.current_id += 1
            return self.word_to_id[word]

    def save_lexicon_file(self):
        with open(self.lexicon_file_path, "w", encoding="utf-8") as file:
            json.dump(self.word_to_id, file)


class URLResolver:
    def __init__(self):
        self.checksums_file_path = "Forward_Index/checksums.json"
        self.url_checksums = self.load_checksums_file()

    def load_checksums_file(self):
        try:
            with open(self.checksums_file_path, "r") as file:
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
        sorted_data = dict(sorted(self.url_checksums.items(), key=lambda x: x[0]))
        with open(self.checksums_file_path, "w") as file:
            json.dump(sorted_data, file)


class InvertedIndex:
    # constructor
    def __init__(self):
        # number of barrels for inverted index
        self.number_of_inverted_index_barrels = 3000

        # list for storing the data to be stored in each barrel
        self.inverted_indices = {}

    # function for saving each barrel data in the corresponding barrel file
    def save_inverted_index_file(self, key, value):
        # Write inverted index to a JSON file
        with open(
            f"Inverted_Index/Inverted_index_files/inverted_index_barrel_{key + 1}.json",
            "w",
        ) as json_file:
            json.dump(value, json_file)

    # function that calls each barrel file one by one and then saves them
    def save_all_inverted_index_files(self):
        for key, value in self.inverted_indices.items():
            self.save_inverted_index_file(key, value)

    # function to load the inverted index file if already exists, else creates a dictionary for inverted index
    def load_inverted_index(self, path):
        try:
            with open(path, "r") as file:
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

                # converting the word id into int
                int_word_id = int(word_id)

                # converting word id back to string
                word_id = str(word_id)

                # getting the frequency
                frequency = word.get("fr")

                # getting the position
                positions = word.get("ps")

                # formula for deciding the barrel in which the word data will be stored
                barrel = int_word_id % self.number_of_inverted_index_barrels

                # check if the inverted index for this barrel is already loaded, then do not reload
                if barrel not in self.inverted_indices:
                    # load the inverted index for this barrel
                    # word_data_in_barrel =
                    self.inverted_indices[barrel] = self.load_inverted_index(
                        f"Inverted_Index/Inverted_index_files/inverted_index_barrel_{barrel + 1}.json"
                    )

                if word_id is not None:
                    # if the inverted index file is empty, initialize it with a key named word_ID
                    if "word_ID" not in self.inverted_indices[barrel]:
                        self.inverted_indices[barrel]["word_ID"] = {}
                    # if word is already not present in the inverted index, then create its key
                    if word_id not in self.inverted_indices[barrel]["word_ID"]:
                        self.inverted_indices[barrel]["word_ID"][word_id] = {}
                    # if a document id for a given word is already present, don't duplicate. else add the details for word in a document in a dictionary
                    if doc_id not in self.inverted_indices[barrel]["word_ID"][word_id]:
                        word_info = {"fr": frequency, "ps": positions}
                        # add the details of the word for that document in the inverted index of the word
                        self.inverted_indices[barrel]["word_ID"][word_id][doc_id] = word_info


# setting up the english stop words from the NLTK
stop_words = set(stopwords.words("english"))

# object for the lemmatizer class
lemmatizer = WordNetLemmatizer()

# list for storing the data as forward index to create the inverted index later on
forward_index_data = []

# initializing the constructor for the Lexicon class
lex = Lexicon()

# initializing the constructor for the Doc id and url mapping class
docid_url_mapping = Docid_Url_Mapping()

# initializing the constructor for the Doc id and date mapping class
docid_date_mapping = Docid_Date_Mapping()

# Initializing the constructor for the URLResolver class
url_resolver = URLResolver()


# deleting the temporary file created
def delete_temp_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Temporary file {file_path} deleted successfully.")
        else:
            print(f"File {file_path} does not exist.")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")


@app.route("/add", methods=["POST"])
def add():
    print("API CALLED")
    if "file" not in request.files:
        response = {
            "error": "Invalid request",
            "message": "No file part in the request.",
        }
        return jsonify(response), 400

    uploaded_file = request.files["file"]
    print("file upload hogayi")
    if uploaded_file.filename.endswith(".json"):
        try:
            print("try ke andar aagaya")
            json_dir = "temp/"
            if not os.path.exists(json_dir):
                os.makedirs(json_dir)
            temp_file_path = os.path.join(json_dir, uploaded_file.filename)
            uploaded_file.save(temp_file_path)
            print("File saved")

            json_files = [
                file for file in os.listdir(json_dir) if file.endswith(".json")]

            # Placeholder lists for processing data
            forward_index_data = []  # Placeholder for forward index data

            # Load data from each JSON file one by one
            for json_file in json_files:
                with open(os.path.join(json_dir, json_file), "r") as f:
                    data = json.load(f)
                    for article in data:
                        url = article.get("url")
                        if url.endswith("/"):
                            url = url.rstrip("/")

                        url_checksum = hashlib.blake2s(url.encode()).hexdigest()
                        doc_id = url_resolver.resolve_doc_id(url_checksum)

                        if doc_id is not None:
                            print(
                                f"Article with URL '{url}' already has docID {doc_id}"
                            )
                        else:
                            doc_id = len(url_resolver.url_checksums) + 1
                            url_resolver.add_document(url_checksum, doc_id)
                            print(
                                f"Assigned new docID {doc_id} for article with URL '{url}'"
                            )

                            content = article.get("content")
                            title = article.get("title")
                            date = article.get("date")

                            title_and_content_merged = f"{title} {content}"
                            words_tokenized = word_tokenize(title_and_content_merged)
                            words_tokenized = [
                                word
                                for word in words_tokenized
                                if re.match("^[a-zA-Z0-9_]*$", word)
                            ]
                            words_tokenized = [word.lower() for word in words_tokenized]
                            clean_words = [
                                word
                                for word in words_tokenized
                                if word not in stop_words
                            ]
                            clean_words = [
                                lemmatizer.lemmatize(word) for word in clean_words
                            ]
                            frequency_distribution = FreqDist(clean_words)
                            positions = {}

                            title = title.lower()
                            for word in frequency_distribution.keys():
                                locations = []
                                for pos, w in enumerate(clean_words):
                                    if w == word:
                                        locations.append(pos)
                                mean_position = calculate_mean_position(locations)
                                positions[word] = mean_position

                            article_entry = {"d_id": doc_id, "words": []}

                            docid_url_mapping.add_to_document_index(doc_id, url)
                            docid_date_mapping.add_to_docId_date_file(doc_id, date)

                            for word in frequency_distribution.keys():
                                word_id = lex.get_word_id(word)
                                if word in title:
                                    word_frequency = frequency_distribution[word] + 20
                                else:
                                    word_frequency = frequency_distribution[word]
                                each_word_detail_in_an_article = {
                                    "w_id": word_id,
                                    "fr": word_frequency,
                                    "ps": positions[word],
                                }
                                article_entry["words"].append(
                                    each_word_detail_in_an_article
                                )

                            forward_index_data.append(article_entry)

            # After processing all JSON files
            url_resolver.sort_file_with_respect_to_checksums_and_save()
            lex.save_lexicon_file()
            docid_url_mapping.save_document_index()
            docid_date_mapping.save_docId_date_file()

            generate_inverted_index = InvertedIndex()
            generate_inverted_index.create_inverted_index(forward_index_data)
            generate_inverted_index.save_all_inverted_index_files()
            response = {"message": "Data inserted successfully"}
            print("Data inserted")
            delete_temp_file(temp_file_path)
            return jsonify(response), 200

        except Exception as e:
            error_response = {"error": "That file already exists", "message": str(e)}
            print(e)
            return jsonify(error_response), 201

    else:
        response = {
            "error": "Invalid file type",
            "message": "Only JSON files are allowed.",
        }
        return jsonify(response), 400

if __name__ == "__main__":
    app.run(debug=True, port=8000)
