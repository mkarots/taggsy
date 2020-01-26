import string

from spacy.lang.en.stop_words import STOP_WORDS

from spacy.lang.en import English

nlp = English()

def is_word(word=None):
    if len(word) == 0: return False
    for char in word:
        if not ('a' <= char <='z' or 'A' <= char <= 'Z'):
            return False
    return True

def is_stopword(word=None):
    if len(word) == 0: return False
    return nlp.vocab[word].is_stop


class WordCounter:
    """
    Count frequencies of words
    
    The input is a string containing zero or more 
    sentences
    """
    
    def __init__(self, nlp_lang=None, word_map=None):
        self.nlp = nlp_lang if nlp_lang is not None else English()
        self.word_map = word_map if word_map is not None else {}
    
    def count_words(self, text):    
        for sentence in text.split('.'):
            self.count_sentence_words(sentence=sentence)
        self.word_map = {i: self.word_map[i] for i in sorted(self.word_map, key=self.word_map.get, reverse=True)}
        breakpoint()
        return self.word_map
    
    def count_sentence_words(self, sentence):
        for token in sentence.split():
            word = token.strip(string.punctuation)
            if is_word(word=word) and not is_stopword(word):
                if word in self.word_map.keys():
                    self.word_map[word] += 1
                else:
                    self.word_map[word] = 1
