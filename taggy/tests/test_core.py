import unittest

from .context import taggy


class TaggyCoreTests(unittest.TestCase):
    def setUp(self):
        self.taggy = taggy.Taggy()


class TestAddText(TaggyCoreTests):
    
    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.taggy.add_text(text='')


class TestGetTags(TaggyCoreTests):

    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.taggy.get_tags(document_ids=[])


if __name__ == "__main__":
    unittest.main()