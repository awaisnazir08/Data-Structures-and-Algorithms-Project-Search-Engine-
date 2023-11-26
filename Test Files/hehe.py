import json
import re
import nltk
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

# Read data from the JSON file
# (Assuming '21stcenturywire.json' contains your input data)
with open('nela-gt-2022/newsdata/21stcenturywire.json', 'r') as file:
    data = json.load(file)

lex = Lexicon()

# Extract words from each dictionary item and store word-to-ID mappings
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

# Write the updated word-to-ID mappings to new.json
with open('new.json', 'w') as file:
    json.dump(lex.word_to_id, file, indent=2)
