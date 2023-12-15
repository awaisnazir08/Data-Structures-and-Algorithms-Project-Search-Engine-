import json
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Set up NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

class Lexicon:
    def __init__(self):
        self.word_to_id = {}
        self.current_id = 1

        # Load existing data from new.json (if exists)
        try:
            with open('new.json', 'r') as file:
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

# Function to count the total number of objects in JSON files
def count_objects(folder_path):
    total_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    num_objects = len(data)
                    total_count += num_objects

                    if total_count >= 100000:
                        return True

                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")
                    continue

    return False  # Did not reach 100,000 objects

lex = Lexicon()
folder_path = 'nela-gt-2022/newsdata'  # Folder containing JSON files

# Extract words from JSON files in the folder and store word-to-ID mappings
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                title_words = item.get('title', '')
                content_words = item.get('content', '')
                combined_text = title_words + ' ' + content_words

                # Tokenize the text using NLTK's word tokenizer
                words_tokenized = word_tokenize(combined_text)

                # Remove punctuation and special characters, lowercase, remove stop words, and lemmatize
                clean_words = [lemmatizer.lemmatize(word.lower()) for word in words_tokenized if word.isalnum() and word.lower() not in stop_words]

                # Store the cleaned words in the lexicon
                for word in clean_words:
                    word_id = lex.get_word_id(word)

        # Check if total objects reach 100,000
        if count_objects(folder_path):
            break

# Write the updated word-to-ID mappings to new.json
with open('wordIDs.json', 'w') as file:
    json.dump(lex.word_to_id, file, indent=2)
