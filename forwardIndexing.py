import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

with open("./nela-gt-2022/newsdata/21stcenturywire.json", "r") as f:
    data = json.load(f)

stop_words = set(stopwords.words('english'))

for article in data: 
    content = article.get('content')
    title = article.get('title')
    text_to_index = f"{title} {content}"
    words_tokenized = word_tokenize(text_to_index)
    fd = FreqDist(words_tokenized)
    tokenize_words_without_stop_words = []
    for word in words_tokenized:
        if word not in stop_words:
            tokenize_words_without_stop_words.append(word.lower())


# print(fd.most_common(5))

# print(f"{word_tokenized} {len(word_tokenized)}\n\n")
# print(len(stop_words))
# print(stop_words)




# print(tokenize_words_without_stop_words, len(tokenize_words_without_stop_words))