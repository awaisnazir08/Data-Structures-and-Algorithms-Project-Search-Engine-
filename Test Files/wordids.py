class Lexicon:
    def __init__(self):
        self.word_to_id = {}
        self.current_id = 1

    def get_word_id(self, word):
        if word in self.word_to_id:
            return self.word_to_id[word]
        else:
            self.word_to_id[word] = self.current_id
            self.current_id += 1
            return self.word_to_id[word]
dataset = ["apple", "banana", "apple", "orange", "banana", "apple"]

lex = Lexicon()
for word in dataset:
    word_id = lex.get_word_id(word)
    print(f"Word: {word} \t WordID: {word_id}")
