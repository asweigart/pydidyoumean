import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import pydidyoumean

runningOnPython2 = sys.version_info[0] == 2

class TestGeneral(unittest.TestCase):

    def test_levenshtein(self):
        self.assertEqual(pydidyoumean.levenshtein('abc', 'abc'), 0)
        self.assertEqual(pydidyoumean.levenshtein('abc', 'bc'), 1)
        self.assertEqual(pydidyoumean.levenshtein('abc', 'ac'), 1)
        self.assertEqual(pydidyoumean.levenshtein('abc', 'ab'), 1)
        self.assertEqual(pydidyoumean.levenshtein('abc', 'c'), 2)


if __name__ == '__main__':
    unittest.main()
