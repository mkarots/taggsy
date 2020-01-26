import unittest

from .context import taggy


class TaggyCoreTests(unittest.TestCase):
    
    def __init__(self):
        super().__init__()
        self.tag_engine = taggy.TagEngine()
    


class TestAddText(TaggyCoreTests):
    
    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.tag_engine.add_text(text='')


class TestGetTags(TaggyCoreTests):

    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.tag_engine.get_tags(document_ids=[])


if __name__ == "__main__":
    unittest.main()