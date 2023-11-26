import json
import re
import os
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

# Set up NLTK
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


# Directory containing JSON files
json_dir = "./nela-gt-2022/newsdata"  # Replace with your actual path

# Get all JSON files in the directory
json_files = [file for file in os.listdir(json_dir) if file.endswith(".json")]

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Create a CSV file for storing the information
csv_file_path = 'forward_indexing.csv'
csv_columns = ['doc_id', 'word', 'frequency', 'positions']

article_id = 0

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    csv_writer.writeheader()

    # Process each JSON file
    for json_file in json_files:
        # Load data from JSON file
        with open(os.path.join(json_dir, json_file), "r") as f:
            data = json.load(f)
            for article in data:
                content = article.get('content')
                title = article.get('title')
                doc_id = article.get('id')
                url = article.get('url')
                title_and_content_merged = f"{title} {content}"
                words_tokenized = word_tokenize(title_and_content_merged)
                
                # Remove special characters, dots, etc.
                words_tokenized = [word for word in words_tokenized if word.isalpha()]
                # words_tokenized = re.sub(r"[^\w\s]", "", title_and_content_merged)

                
                # Convert to lowercase
                words_tokenized = [word.lower() for word in words_tokenized]

                # Remove stop words
                clean_words = [word for word in words_tokenized if word not in stop_words]
                
                # Lemmatization
                clean_words = [lemmatizer.lemmatize(word) for word in clean_words]

                # Calculate word frequency and occurrence positions
                freq_dist = FreqDist(clean_words)
                positions = [pos for pos, w in enumerate(clean_words) if w == word]
                for word, freq in freq_dist.items():
                    csv_writer.writerow({'doc_id': article_id, 'word': word, 'frequency': freq, 'positions': positions})
                article_id+=1