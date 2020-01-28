import json
import os
import unittest
from unittest import mock

from .context import taggsy
from taggsy import Document, Word, Sentence, DocumentComponent
from taggsy.helpers import filter_stopwords


class TaggyCoreTestCase(unittest.TestCase):
    '''
    Test helpers
    '''

    def create_word(self, text=None, sentence_text=None, document=None):
        return Word(text=text, sentence_text=sentence_text, document=document)

    def create_sentence(self, text=None, words=None, document=None):
        return Sentence(text=text, words=words, document=document)
    
    def create_document(self, name=None, sentences=None, text=None):
        return Document(name=name, text=text, sentences=sentences)
    
    def get_docs_from_json(self, path):
        with open(path, 'r') as f:
           quotes = json.loads(f.read())
        documents = [item['quote'] for item in quotes['quotes']]
        return documents


class CoreTestCase(TaggyCoreTestCase):
   
    def setUp(self):
        super().setUp()
        self.core = taggsy.Core()
    
    def test_simple_documents(self):
        '''
        Ensure adding docs works as expected
        '''
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        self.core.add_document(doc=doc1)
        self.core.add_document(doc=doc2)
        self.assertEqual(len(self.core.documents), 2)

    def test_simple_documents_result(self):
        '''
        Ensure the result is as expected for a simple case
        '''
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc1_name = self.core.add_document(doc=doc1)
        doc2_name = self.core.add_document(doc=doc2)
        expectedResult = {'philosophy': {'count': 2, 'docs': [doc1_name, doc2_name], 'sentences':[doc1, doc2]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_simple_documents_result_second(self):
        '''
        Ensure the result is as expected for a simple case
        '''
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc1_name = self.core.add_document(doc=doc1)
        self.core.most_common()
        doc2_name = self.core.add_document(doc=doc2)
        expectedResult = {'philosophy': {'count': 2, 'docs': [doc1_name, doc2_name], 'sentences':[doc1, doc2]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_multiple_documents(self):
        '''
        Ensure correctness when docs > 2
        '''
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc3 = 'Philosophy is nice'
        doc1_name = self.core.add_document(doc=doc1)
        doc2_name = self.core.add_document(doc=doc2)
        doc3_name = self.core.add_document(doc=doc3)
        expectedResult = {'philosophy': {'count': 3, 'docs': [doc1_name, doc2_name, doc3_name], 'sentences':[doc1, doc2, doc3]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_with_path(self):
        '''
        Ensure that adding documents from paths works as expected
        '''
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
        '''
        Ensure add_document is called with the right number of arguments when
        add_documents is called
        '''
        docs = ['a', 'b', 'c']
        with mock.patch('taggsy.Core.add_document') as mock_add_document:
            self.core.add_documents(docs)
            mock_add_document.assert_has_calls(calls=[mock.call(item) for item in docs])
    
    def test_example_imagination(self):
        '''
        Ensure 'imagination' is picked up
        '''
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'test_imagination.json')
        documents = self.get_docs_from_json(path=path)
        self.core.add_documents(documents)
        res = self.core.most_common()
        self.assertIn('imagination', res.keys())

    def test_example_inspiration(self):
        '''
        Ensure 'inspiration' is picked up
        '''
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'test_inspiration.json')
        documents = self.get_docs_from_json(path=path)
        self.core.add_documents(documents)
        res = self.core.most_common()
        self.assertIn('inspiration', res.keys())

    def test_example_civilisation(self):
        '''
        Ensure 'civilization' is picked up
        '''
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'test_civilisation.json')
        documents = self.get_docs_from_json(path=path)
        self.core.add_documents(documents)
        res = self.core.most_common()
        self.assertIn('civilization', res.keys())


class DocumentTestCase(TaggyCoreTestCase):
    
    def test_document_from_path(self):
        '''
        Test Document.from_path instantiation
        '''
        path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'doca.txt')
        with open(path1, 'r') as f:
            text = f.read()
        document = Document.from_path(path1)
        expected_words = [self.create_word(text=word, sentence_text=text, document=self.create_document()) for word in filter_stopwords(words=text.split())]
        expected_sentences = [self.create_sentence(words=expected_words, text=sentence) for sentence in [text]]
        expected_document = Document(name='doca.txt', sentences=expected_sentences, text=text)       
        self.assertEqual(expected_document, document)


class SentenceTestCase(TaggyCoreTestCase):
 
    def test_sentence_from_text(self):
        '''
        Test Sentence.from_text instantiation
        '''
        text = 'This is a sentence'
        sentence = Sentence.from_text(text=text, document=None)
        expectedSentence = Sentence(text=text, words=[Word(text='sentence', sentence_text=text)])
        self.assertEqual(sentence, expectedSentence)


class WordTestCase(TaggyCoreTestCase):

    def test_word_from_text(self):
        '''
        Test Word.from_text instantiation
        '''
        text = 'word'
        expectedWord = Word(text=text)
        self.assertEqual(expectedWord, Word.from_text(text=text))
        

class DocumentComponentTestCase(TaggyCoreTestCase):
    """
    Ensure that calling compute() twice on the component causes _compute to be only called once
    """
    def test_document_component(self):
        component = DocumentComponent()
        with mock.patch('taggsy.DocumentComponent._compute') as mocked_compute:
            component.compute()
            component.compute()
            mocked_compute.assert_called_once()
    

if __name__ == "__main__":
    unittest.main()