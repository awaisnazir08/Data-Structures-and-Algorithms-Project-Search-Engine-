import json
from collections import defaultdict
import re
from nltk.corpus import stopwords

# Download the NLTK stop words data if not already present
import nltk
nltk.download('stopwords')

class ForwardIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.keywords_dict = {}

    def add_document(self, document):
        doc_id = document.get("id")
        title = document.get("title")
        content = document.get("content")

        # Combine title and content
        text_to_index = f"{title} {content}"

        # Tokenize the text (split into words)
        words = text_to_index.lower().split()

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

        # Extract main keywords
        keywords = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in words]

        # Store keywords in the dictionary for each article
        self.keywords_dict[doc_id] = keywords

        # Add each keyword to the forward index for the document
        for keyword in keywords:
            self.index[keyword].append(doc_id)

    def search(self, query):
        # Convert the query to lowercase and tokenize
        query_words = query.lower().split()

        # Find documents that contain all query words
        result = set(self.index[query_words[0]])
        for word in query_words[1:]:
            result = result.intersection(self.index[word])

        return result

# Example usage:
if __name__ == "__main__":
    # Load your JSON data
    with open("./nela-gt-2022/newsdata/21stcenturywire.json", "r") as file:
        data = json.load(file)

    # Create a ForwardIndex instance
    forward_index = ForwardIndex()

    # Add documents to the forward index
    for document in data:
        forward_index.add_document(document)

    # Example search
    query = "Climate"
    result = forward_index.search(query)

    # Print the result
    print("Search result for query '{}':".format(query))
    for doc_id in result:
        print(doc_id)

    # Print the keywords for each document
    print("\nKeywords for each document:")
    for doc_id, keywords in forward_index.keywords_dict.items():
        print(f"Document ID: {doc_id}, Keywords: {keywords}")
