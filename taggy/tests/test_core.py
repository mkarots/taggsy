import json
import os
import unittest

from .context import taggy
from taggy import Document, Word, Sentence


class TaggyCoreTestCase(unittest.TestCase):

    def create_mock(spec=None):
        return unittest.mock.create_autospec(spec=spec)

    def create_word(self, text=None, sentence_text=None, document=None):
        return Word(text=text, sentence_text=sentence_text, document=document)

    def create_sentence(self, text=None, words=None, document=None):
        return Sentence(text=text, words=words, document=document)
    
    # def create_document(self, ):

class CoreTestCase(TaggyCoreTestCase):
    """
    Test core functionality
    """
    def setUp(self):
        self.core = taggy.Core()
    
    def test_simple_documents(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        self.core.add_document(doc=doc1)
        self.core.add_document(doc=doc2)
        self.assertEqual(len(self.core.documents), 2)

    def test_simple_documents_result(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc1_name = self.core.add_document(doc=doc1)
        doc2_name = self.core.add_document(doc=doc2)
        expectedResult = {'philosophy': {'count': 2, 'docs': [doc1_name, doc2_name], 'sentences':[doc1, doc2]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_simple_documents_result_second(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc1_name = self.core.add_document(doc=doc1)
        self.core.most_common()
        doc2_name = self.core.add_document(doc=doc2)
        expectedResult = {'philosophy': {'count': 2, 'docs': [doc1_name, doc2_name], 'sentences':[doc1, doc2]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_multiple_documents(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc3 = 'Philosophy is nice'
        doc1_name = self.core.add_document(doc=doc1)
        doc2_name = self.core.add_document(doc=doc2)
        doc3_name = self.core.add_document(doc=doc3)
        expectedResult = {'philosophy': {'count': 3, 'docs': [doc1_name, doc2_name, doc3_name], 'sentences':[doc1, doc2, doc3]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_with_path(self):
        path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'doca.txt')
        path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'docb.txt')
        self.core.add_document(doc=path1)
        self.core.add_document(doc=path2)
        res = self.core.most_common()
        expectedResult = {
            'glitters': {'count': 2, 'docs': ['doca.txt', 'docb.txt'], 'sentences': ['Not all that is gold glitters', 'Not all that glitters is gold']},
            'gold': {'count': 2, 'docs': ['doca.txt', 'docb.txt'], 'sentences': ['Not all that is gold glitters', 'Not all that glitters is gold']}}
        self.assertEqual(res, expectedResult)


    def test_add_documents(self):
        

    def test_examples(self):
        """
        test imagination.json
        """
        path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'test_imagination.json')
        with open(path1, 'r') as f:
           quotes = json.loads(f.read())
        documents = [item['quote'] for item in quotes['quotes']]
        self.core.add_documents(documents)
        res = self.core.most_common()
        self.assertIn('imagination', res.keys())

    def test_examples(self):
        """
        test inspiration.json
        """
        path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'test_inspiration.json')
        with open(path1, 'r') as f:
           quotes = json.loads(f.read())
        documents = [item['quote'] for item in quotes['quotes']]
        self.core.add_documents(documents)
        res = self.core.most_common()
        self.assertIn('inspiration', res.keys())


class DocumentTestCase(TaggyCoreTestCase):

    def test_document_from_path(self):
        path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'doca.txt')
        document = Document.from_path(path1)
        expectedDocument = Document(sentences=[])       
        self.maxDiff = None 
        self.assertEqual(expectedDocument, document)

class SentenceTestCase(TaggyCoreTestCase):
    """
    test sentence from_text
    """
    def test_sentence(self):
        pass

class WordTestCase(TaggyCoreTestCase):
    """
    test word from text
    """
    def test_word_from_text(self):
        text = 'word'
        expectedWord = Word(text=text)
        self.assertEqual(expectedWord, Word.from_text(text=text))
        

class CoreModelTestCase():
    """
    test compute functionality
    """
    def test_core_model(self):
        pass


if __name__ == "__main__":
    unittest.main()