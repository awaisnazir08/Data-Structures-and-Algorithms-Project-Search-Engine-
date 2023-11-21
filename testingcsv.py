import json
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

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Create a CSV file for storing the information
csv_file_path = 'word_frequency_and_positions.csv'
csv_columns = ['doc_id', 'word', 'frequency', 'positions']
count = 0
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    csv_writer.writeheader()

    with open("./nela-gt-2022/newsdata/21stcenturywire.json", "r") as f:
        data = json.load(f)

        for article in data:
            content = article.get('content')
            title = article.get('title')
            doc_id = article.get('id')
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
            freq_dist = FreqDist(clean_words)
            for word, freq in freq_dist.items():
                positions = [pos for pos, w in enumerate(clean_words) if w == word]
                csv_writer.writerow({'doc_id': doc_id, 'word': word, 'frequency': freq, 'positions': positions})
