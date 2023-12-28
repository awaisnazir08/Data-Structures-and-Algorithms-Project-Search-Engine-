import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import heapq
import sys
import time

#function to load the lexicon for finding the word id corresponding to the searched word
def load_Lexicon():
    file_path = "Forward_Index/Lexicon.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None  

#function to load the document index file for finding the urls of documents corresponding to the searched word
def load_documentIndex():
    file_path = "Forward_Index/document_index.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

#function to load the file for finding the dates of documents published corresponding to the searched word
def load_document_date_file():
    file_path = "Forward_Index/docId_date_mapping.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

#function to load the relevant barrel into ram for finding the document ids and data corresponding to the searched word
def load_inverted_index_barrel(path):
    try: 
        with open(path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

'''
function for getting all the documents along with their ids and data
for those documents that contain the searched word
'''
def get_documents(word_id, word_data_in_barrel):
    if str(word_id) in word_data_in_barrel["word_ID"]:
        word_data = word_data_in_barrel["word_ID"][str(word_id)]
        return word_data
    else:
        return {}


#setting up the english stop words from the NLTK
stop_words = set(stopwords.words('english'))

#object for the lemmatizer class
lemmatizer = WordNetLemmatizer()

#object for loading the lexicon dictionary 
lexicon_dictionary = load_Lexicon()

#object for loading the file that contains the documents are their urls
document_urls = load_documentIndex()

#dictionary for storing the data of each barrel that needs to be loaded for getting the word data
loaded_inverted_indices = {}

#getting the searched input query from the user
query = input("Enter the query to search: ")

#starting the timer to calculate the execution time
start_time = time.time()

#tokenizing the combined words
query_tokenized = word_tokenize(query)

#remove special characters, dots, etc.
query_tokenized = [word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

#convert to lowercase
query_tokenized = [word.lower() for word in query_tokenized]

#remove stop words
clean_query = [word for word in query_tokenized if word not in stop_words]

#lemmatization
clean_query = [lemmatizer.lemmatize(word) for word in clean_query]


for word in clean_query:
    try: 
        word_id = lexicon_dictionary[word]
    except:
        print(f'{word} is not present in any document!')
        continue
    
    #getting the relevant barrel id that contains the searched word
    barrel_id = word_id % 3000

    #check if the inverted index for this barrel is already loaded, then do not reload
    if barrel_id in loaded_inverted_indices:
        word_data_in_barrel = loaded_inverted_indices[barrel_id]
    else:
        #load the inverted index for this barrel
        word_data_in_barrel = load_inverted_index_barrel(f'Inverted_Index/Inverted_index_files/inverted_index_barrel_{barrel_id + 1}.json')
        loaded_inverted_indices[barrel_id] = word_data_in_barrel

    #getting the information for all the documents that have a particular word searched
    documents = get_documents(word_id, word_data_in_barrel)
    
    #dictionary that will store the documents along with their scores for ranking 
    document_score = {}
    #scoring the documents based on the number of words they contain out of the number of searched words
    for document in documents.keys():

        '''
        if document appears first time, then give it a score one
        this means that the document so far has only one word in it out of the 
        total number of words searched
        '''
        if document not in document_score:
            document_score[document] = {"count": 1, "values": [documents[document]]}
        else:
            '''
            increasing the score of the documents by one everytime
            they appear again, this means they have more words in them
            that have been searched, so they will be scored higher
            '''
            document_score[document]["count"] += 1
            document_score[document]["values"].append(documents[document])

#condition to check if no document appears, this means that the searched query has no relevant articles available
if(len(document_score)== 0):
    print("The searched query is not present in any document!\nPlease search for other words..!!")
    sys.exit()

#getting the max scored document
max_count_document = max(document_score.items(), key=lambda x: x[1]["count"])

#getting the score of the max scored document
max_count = max_count_document[1]["count"]
print(max_count)

#variable that keeps track of the number of documents that have been displayed
documents_shown = 0

#if the number of documents shown exceed 30 or no more documents are left, then stop
while(documents_shown < 30 and max_count >=1):

    #a list that will store the documents of same score and then will be used for sorting
    priority_queue = []

    #loop to iterate over each document that has been retreived
    for doc in document_score.items():
        if doc[1]["count"] == max_count:
            getting_frequencies = doc[1]['values']
            frequency = 0

            '''
            summing up the frequencies of each document that has the same
            number of words out of the number of words searched, 
            this is being used for ranking
            '''
            for value in getting_frequencies:
                frequency += value['fr']

            #pushing the document ids into heap based on the frequency in descending order
            heapq.heappush(priority_queue, (-frequency, doc[0]))

    #decreasing the count
    max_count -= 1

    #popping the document ids from the heap
    for _ in range(len(priority_queue)):
        if priority_queue:
            if(documents_shown >= 30):
                break
            frequency, document_id = heapq.heappop(priority_queue)
            #accessing the document index to get the document urls and then displaying them on terminal
            document_url = document_urls[document_id]
            print(document_id, " ", -frequency, " ", document_url)
            documents_shown += 1

#ending the program execution time
end_time = time.time()

#calculating the time taken
execution_time = end_time - start_time

#displaying the time taken by the code to run
print(f"Code took {execution_time:.6f} seconds to run.")
