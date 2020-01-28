from unittest import TestCase

from .context import taggy


class TestFilterStopwords(TestCase):

    def test_filters_out_stopwords(self):
        word_list = ['this', 'is', 'are']
        filtered_list = taggy.helpers.filter_stopwords(words=word_list)
        self.assertEqual(filtered_list, [])

    def test_does_not_filter_out_non_stopwords(self):
        word_list = ['word', 'clarity']
        filtered_list = taggy.helpers.filter_stopwords(words=word_list)
        self.assertEqual(filtered_list, word_list)

if __name__ == "__main__":
    unittest.main()
    
