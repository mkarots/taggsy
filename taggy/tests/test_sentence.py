from .context import taggy

import unittest


class BasicTestSuite(unittest.TestCase):
    """ Basic Test Cases """ 

    def test_true_value(self):
        assert True


if __name__ == "__main__":
    unittest.main()
