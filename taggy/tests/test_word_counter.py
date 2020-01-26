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
        string = 'science.philosophy'
        expectedResult = {'science': 1, 'philosophy': 1}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)

    def test_medium_sentence(self):
        string = 'Philosophy is a really cool hobby'
        expectedResult = {'Philosophy': 1, 'cool': 1, 'hobby': 1}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)
    
    def test_punctuation_only(self):
        string = '..'
        expectedResult = {}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)

    def test_symbols(self):
        string = '.^.'
        expectedResult = {}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)
    
    def test_order(self):
        string='philosophy, philosophy, science'
        expectedResult = {'philosophy': 2, 'science': 1}
        self.assertEqual(self.word_counter.count_words(text=string), expectedResult)

    def test_quote(self):
        quote="Where there's a will there's a way"
        expectedResult = {'way': 1}
        self.assertEqual(self.word_counter.count_words(text=quote), expectedResult)

    def test_tolkien_quote(self):
        quote="Not all those who wander are lost"
        expectedResult = {'wander': 1, 'lost': 1}
        self.assertEqual(self.word_counter.count_words(text=quote), expectedResult)

    def test_test_doc(self):
        text = open('tests/docs/doc1.txt', 'r').read()
        expectedResult = {'wander': 1, 'lost': 1}
        self.maxDiff = None
        self.assertEqual(self.word_counter.count_words(text=text), expectedResult)


if __name__ == "__main__":
    unittest.main()