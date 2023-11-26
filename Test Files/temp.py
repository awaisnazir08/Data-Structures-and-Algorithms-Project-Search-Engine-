import json
import nltk
from nltk.corpus import stopwords
import string
import re

nltk.download('stopwords')

def preprocess_text(text):
    text = re.sub(r'(\\u\d+)', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join([i for i in text if not i.isdigit()])
    return text

def create_forward_index_with_preprocessing(data):
    forward_index = {}
    stop_words = set(stopwords.words('english'))

    for idx, item in enumerate(data):
        title_words = [word.lower() for word in preprocess_text(item['title']).split() if word.lower() not in stop_words]
        content_words = [word.lower() for word in preprocess_text(item['content']).split() if word.lower() not in stop_words]
        words = title_words + content_words

        for word in words:
            if word not in forward_index:
                forward_index[word] = []
            forward_index[word].append(idx)

    return forward_index

with open("Data-Structures-and-Algorithms-Project\\nela-gt-2022\\newsdata\\369news.json", "r") as f:
    data = json.load(f)

forward_index_with_preprocessing = create_forward_index_with_preprocessing(data)

with open('forward_index_with_preprocessing.json', 'w') as file:
    json.dump(forward_index_with_preprocessing, file, indent=4)
