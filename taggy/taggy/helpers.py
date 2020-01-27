import string
import random

from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

nlp = English()

def is_word(word=None):
    return word.isalpha

def is_stopword(word=None):
    if len(word) == 0: return False
    return nlp.vocab[word].is_stop

def filter_stopwords(words):
    """Filter out non words and stop words"""
    filtered_stopwords = []
    for word in words:
        word = word.strip().lower()
        word = word.translate(str.maketrans('', '', string.punctuation))
        if is_word(word) and not is_stopword(word): filtered_stopwords.append(word)
    return filtered_stopwords

def generate_random_string(string_length=6):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))