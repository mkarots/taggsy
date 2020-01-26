from .context import taggy
import unittest

class WordCounterTestCase(unittest.TestCase):
    
    def setUp(self):
        self.word_counter = taggy.WordCounter()
    
    def test_empty_string(self):
        string = ''
        expectedResult = {}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)

    def test_single_word(self):
        string = 'word'
        expectedResult = {'word': 1}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)

    def test_two_sentence_single(self):
        string = 'one.two'
        expectedResult = {'one': 1, 'two': 1}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)

    def test_medium_sentence(self):
        string='Philosophy is cool'
        expectedResult = {'Philosophy': 1, 'is': 1, 'cool': 1}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)