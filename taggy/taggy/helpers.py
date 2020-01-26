
class WordCounter:
    """
    Count frequencies of words
    
    The input is a string containing zero or more 
    sentences

    """
    
    def __init__(self, word_map=None):
        self.word_map = word_map if word_map is not None else {}

    def count_words(self, text):    
        for sentence in text.split('.'):
            self.count_sentence_words(sentence=sentence)
        return self.word_map
    
    def count_sentence_words(self, sentence):
        for word in sentence.split():
            if word in self.word_map.keys():
                self.word_map[word] += 1
            else:
                self.word_map[word] = 1