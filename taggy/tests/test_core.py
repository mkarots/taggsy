import unittest

from .context import taggy


class TaggyCoreTestCase(unittest.TestCase):
    
    def create_mock(spec=None):
        return unittest.mock.create_autospec(spec=spec)


class CoreTestCase(TaggyCoreTestCase):
    """
    Test core functionality
    """
    def setUp(self):
        self.core = taggy.Core()
    
    def test_simple_documents(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        self.core.add_document(doc1)
        self.core.add_document(doc2)
        self.assertEqual(len(self.core.documents), 2)

    def test_simple_documents_result(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc1_name = self.core.add_document(doc1)
        doc2_name = self.core.add_document(doc2)
        expectedResult = {'philosophy': {'docs': [doc1_name, doc2_name], 'sentences':[doc1, doc2]}}
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_simple_documents_result_second(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc1_name = self.core.add_document(doc1)
        self.core.most_common()
        doc2_name = self.core.add_document(doc2)
        expectedResult = {'philosophy': {'docs': [doc1_name, doc2_name], 'sentences':[doc1, doc2]}}
        self.maxDiff = None
        self.assertEqual(self.core.most_common(), expectedResult)

    def test_multiple_documents(self):
        doc1 = 'Philosophy is cool'
        doc2 = 'Philosophy is awesome'
        doc3 = 'Philosophy is nice'
        doc1_name = self.core.add_document(doc1)
        doc2_name = self.core.add_document(doc2)
        doc3_name = self.core.add_document(doc3)
        expectedResult = {'philosophy': {'docs': [doc1_name, doc2_name, doc3_name], 'sentences':[doc1, doc2, doc3]}}
        self.assertEqual(self.core.most_common(), expectedResult)


class DocumentTestCase(TaggyCoreTestCase):

    def test_document(self):
        pass


class SentenceTestCase(TaggyCoreTestCase):
    pass


class WordTestCase(TaggyCoreTestCase):
    pass




if __name__ == "__main__":
    unittest.main()