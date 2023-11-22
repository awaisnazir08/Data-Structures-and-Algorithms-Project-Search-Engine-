import nltk

# nltk.download('wordnet')
text = """Welcome to Programming knowledge. Lets start with our first start tutorial on NLTK. We shall learn the basics of NLTK here."""

from nltk.tokenize import word_tokenize
word_tokenized = word_tokenize(text)
# print(f"{word_tokenized} {len(word_tokenized)}\n\n")
# from nltk.tokenize import sent_tokenize
# sent_tokenized = sent_tokenize(text)

from nltk.probability import FreqDist
fd = FreqDist(word_tokenized)

# print(fd.most_common(5))
print(fd.keys())

# from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))
# # print(len(stop_words))
# # print(stop_words)

# tokenize_words_without_stop_words = []

# for word in word_tokenized:
#     if word not in stop_words:
#         tokenize_words_without_stop_words.append(word)

# print(tokenize_words_without_stop_words, len(tokenize_words_without_stop_words))

# positions = {word: [pos for pos, w in enumerate(clean_words) if w == word] for word in freq_dist.keys()}

# positions = {}
# for word in freq_dist.keys():
#     positions[word] = [position for position, w in enumerate(clean_words) if w == word]