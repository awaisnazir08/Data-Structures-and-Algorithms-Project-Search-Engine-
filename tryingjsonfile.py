import json
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

# Set up NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Create a dictionary for storing the information
forward_index = {"forward_index": []}

# Directory containing JSON files
json_dir = "./nela-gt-2022/newsdata/369news.json"  # Replace with your actual path

article_id = 0

with open(json_dir, "r") as f:
    data = json.load(f)
    for article in data:
        content = article.get('content')
        title = article.get('title')
        doc_id = article.get('id')
        url = article.get('url')
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
        #it gives us all the unique words in the lemmatized list of words
        frequency_distribution = FreqDist(clean_words)

        #initializing a new dictionary to store the positions for each word in the json file
        positions = {}

        #finding the position of each word
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
        # a json object for each word, its details, these will be stored in the list of words in main json object
        for word in frequency_distribution.keys():
            each_word_detail_in_an_article = {
                "word":word,
                "frequency": frequency_distribution[word],
                "positions": positions[word]
            }
            article_entry["words"].append(each_word_detail_in_an_article)

        # Add the entry to the forward_index dictionary
        forward_index["forward_index"].append(article_entry)

# Write the JSON structure to a file
json_file_path = 'forward_indexing.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(forward_index, json_file, indent='\t')
print(len(json_file_path))
