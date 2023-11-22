import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# # Directory containing JSON files
# json_dir = "./nela-gt-2022/newsdata"  # Replace with your actual path

# count = 0
# # Get all JSON files in the directory
# json_files = [file for file in os.listdir(json_dir) if file.endswith(".json")]
# print(len(json_files))
# # Process each JSON file
# for json_file in json_files:
#     # Load data from JSON file
#     with open(os.path.join(json_dir, json_file), "r") as f:
#         data = json.load(f)
#         count+=len(data)

# print(count)


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

with open("./nela-gt-2022/newsdata/21stcenturywire.json", "r") as f:
    data = json.load(f)

for article in data: 
    content = article.get('content')
    title = article.get('title')
    doc_id = article.get('id')
    title_and_content_merged = f"{title} {content}"
    words_tokenized = word_tokenize(title_and_content_merged)
    clean_words = []

    #remove special characters, dots etc
    words_tokenized = [word for word in words_tokenized if word.isalpha()]

    #convert to lower case
    words_tokenized = [word.lower() for word in words_tokenized]

    #remove special characters
    clean_words = [word for word in words_tokenized if word not in stop_words]
    # for word in words_tokenized:
    #     if word not in stop_words:
    #         clean_words.append(word)
    
    #applying lemmatization
    clean_words =  [lemmatizer.lemmatize(word) for word in clean_words]

    fd = FreqDist(words_tokenized)



# print(fd.most_common(5))

# print(f"{word_tokenized} {len(word_tokenized)}\n\n")
# print(len(stop_words))
# print(stop_words)




# print(clean_words, len(clean_words))