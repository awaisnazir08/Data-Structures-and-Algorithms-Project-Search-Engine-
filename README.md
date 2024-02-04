Taazaa Akhbaar is the outcome of collaborative efforts during our third semester of Data Structures and Algorithms at NUST, guided by the esteemed instructor Sir Faisal Shafait. We extend our special thanks to him for providing us with an invaluable opportunity to work on this impactful project. Developed in Python, Taazaa Akhbaar is a sophisticated search engine designed to handle a substantial dataset of 120,000 articles from the Kaggle nela-gt-2022 dataset in JSON format. Alongside my partner Shahzaib, we implemented a variety of features, including support for single and multi-word search queries, dynamic content addition for extra documents, a user-friendly interface, and efficient query handling, all accomplished within milliseconds. The underlying technology stack involves essential libraries such as NLTK, JSON, OS, Hashlib, heapq, and Flask for both backend and frontend development.

The backbone of Taazaa Akhbaar lies in its optimized data structures and components. We utilized hash tables for query management, lists, and dictionaries for forward and backward index files, as well as a max heap (priority queue) and Tim Sort for ranking. The forward index, divided into 2000 barrels for optimal file handling, stores word IDs, doc IDs, word frequency, and position. The inverted index, comprising 3000 barrels, forms the core of the search engine, storing doc IDs, word IDs, position, and frequency. A comprehensive lexicon, housing around 200,000 unique words, and a checksum file, preventing document duplication, add to the efficiency of our system. The custom page ranking algorithm considers word occurrence, frequency, and title position.

Efficiency is a key focus of Taazaa Akhbaar. With constant time O(1) retrieval, we mitigated potential CPU load issues by dividing indexes into barrels, facilitating faster file handling. Taazaa Akhbaar represents a meticulous application of data structures and algorithms, showcasing innovation in search engine technology. We are thrilled to present our project, emphasizing the power of technology in a rapidly evolving digital landscape.
