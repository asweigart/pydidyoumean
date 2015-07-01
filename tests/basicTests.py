import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
import pydidyoumean

runningOnPython2 = sys.version_info[0] == 2

if runningOnPython2:
    from cStringIO import StringIO
else:
    from io import StringIO

class TestGeneral(unittest.TestCase):
    def test_validateTestFolderContents(self):
        self.assertEqual(os.listdir(os.path.dirname(os.path.realpath(__file__))),
                         ['basicTests.py', 'test_file_abc.txt', 'test_file_abcdef.txt', 'test_file_foo.txt'],
                         'Have you changed the contents on the test folder?')

        self.assertTrue(os.path.exists(os.path.join('..', 'setup.py'))) # the setup.py in the root project folder is also used in these tests.

    def test_levenshtein(self):
        testData = (('abc', 'abc', 0), # format: (s1, s2, expectedDistance)
                    ('abc', 'bc', 1),
                    ('abc', 'ac', 1),
                    ('abc', 'ab', 1),
                    ('abc', 'a', 2),
                    ('abc', 'b', 2),
                    ('abc', 'c', 2),
                    ('abc', 'xbc', 1),
                    ('abc', 'axc', 1),
                    ('abc', 'abx', 1),
                    ('abc', 'abcd', 1),
                    ('It was a bright cold day in April, and the clocks were striking thirteen.',
                     'It was a bright COld ay in April, xand the clocs were xstriking thrteen.',
                     7),
                   )

        for s1, s2, expectedDistance in testData:
            actualDistance = pydidyoumean.levenshtein(s1, s2)
            self.assertEqual(expectedDistance, actualDistance,
                'Expected distance between %r and %r was %s, but actually was %s.' % (s1, s2, expectedDistance, actualDistance))

            # reverse order to check for associative equality
            actualDistance = pydidyoumean.levenshtein(s2, s1)
            self.assertEqual(expectedDistance, actualDistance,
                'Expected distance between %r and %r was %s, but actually was %s.' % (s1, s2, expectedDistance, actualDistance))


    def test_printFileSuggestion(self):
        savedStdOut = sys.stdout

        # basic test
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printFileSuggestion('test_file_ab.txt')
        self.assertEqual(mystdout.getvalue(), 'Did you mean test_file_abc.txt?\n')

        # test message arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printFileSuggestion('test_file_ab.txt', message='How about %s?\n')
        self.assertEqual(mystdout.getvalue(), 'How about test_file_abc.txt?\n')

        # test folder arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printFileSuggestion('test_file_ab.txt', folder=os.path.join('..', 'tests'))
        self.assertEqual(mystdout.getvalue(), 'Did you mean test_file_abc.txt?\n')

        sys.stdout = mystdout = StringIO()
        pydidyoumean.printFileSuggestion('setup.py', folder='..', threshold=0, includeIdenticalFilename=True)
        self.assertEqual(mystdout.getvalue(), 'Did you mean setup.py?\n')

        # test threshold arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printFileSuggestion('test_file_ab.txt', threshold=0)
        self.assertEqual(mystdout.getvalue(), '')

        # test includeIdenticalFilename arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printFileSuggestion('test_file_abc.txt', threshold=0, includeIdenticalFilename=True)
        self.assertEqual(mystdout.getvalue(), 'Did you mean test_file_abc.txt?\n')

        sys.stdout = savedStdOut


    def test_getFileSuggestion(self):
        # basic test
        self.assertEqual(pydidyoumean.getFileSuggestion('test_file_ab.txt'),
                         'Did you mean test_file_abc.txt?\n')

        # test message arg
        self.assertEqual(pydidyoumean.getFileSuggestion('test_file_ab.txt', message='How about %s?\n'),
                         'How about test_file_abc.txt?\n')

        # test folder arg

        self.assertEqual(pydidyoumean.getFileSuggestion('test_file_ab.txt', folder=os.path.join('..', 'tests')),
                         'Did you mean test_file_abc.txt?\n')


        self.assertEqual(pydidyoumean.getFileSuggestion('setup.py', folder='..', threshold=0, includeIdenticalFilename=True),
                         'Did you mean setup.py?\n')

        # test threshold arg
        self.assertEqual(pydidyoumean.getFileSuggestion('test_file_ab.txt', threshold=0),
                         '')

        # test includeIdenticalFilename arg
        self.assertEqual(pydidyoumean.getFileSuggestion('test_file_abc.txt', threshold=0, includeIdenticalFilename=True),
                        'Did you mean test_file_abc.txt?\n')


    def test_suggestFile(self):
        # basic test
        self.assertEqual(pydidyoumean.suggestFile('test_file_ab.txt'),
                         'test_file_abc.txt')

        # test folder arg
        self.assertEqual(pydidyoumean.suggestFile('test_file_ab.txt', folder=os.path.join('..', 'tests')),
                         'test_file_abc.txt')


        self.assertEqual(pydidyoumean.suggestFile('setup.py', folder='..', threshold=0, includeIdenticalFilename=True),
                         'setup.py')

        # test threshold arg
        self.assertEqual(pydidyoumean.suggestFile('test_file_ab.txt', threshold=0),
                         None)

        # test includeIdenticalFilename arg
        self.assertEqual(pydidyoumean.suggestFile('test_file_abc.txt', threshold=0, includeIdenticalFilename=True),
                        'test_file_abc.txt')


    def test_suggestAllFiles(self):
        # basic test
        self.assertEqual(list(pydidyoumean.suggestAllFiles('test_file_ab.txt')),
                         ['test_file_abc.txt'])

        # test folder arg
        self.assertEqual(list(pydidyoumean.suggestAllFiles('test_file_ab.txt', folder=os.path.join('..', 'tests'))),
                         ['test_file_abc.txt'])


        self.assertEqual(list(pydidyoumean.suggestAllFiles('setup.py', folder='..', threshold=0, includeIdenticalFilename=True)),
                         ['setup.py'])

        # test threshold arg
        self.assertEqual(list(pydidyoumean.suggestAllFiles('test_file_ab.txt', threshold=0)),
                         [])

        # test includeIdenticalFilename arg
        self.assertEqual(list(pydidyoumean.suggestAllFiles('test_file_abc.txt', threshold=0, includeIdenticalFilename=True)),
                        ['test_file_abc.txt'])


    def test_printSuggestion(self):
        savedStdOut = sys.stdout

        # basic test
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printSuggestion('ab', ['abc', 'abcdef', 'foo'])
        self.assertEqual(mystdout.getvalue(), 'Did you mean abc?\n')

        # test message arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printSuggestion('ab', ['abc', 'abcdef', 'foo'], message='How about %s?\n')
        self.assertEqual(mystdout.getvalue(), 'How about abc?\n')

        # test threshold arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printSuggestion('ab', ['abc', 'abcdef', 'foo'], threshold=0)
        self.assertEqual(mystdout.getvalue(), '')

        # test includeIdenticalName arg
        sys.stdout = mystdout = StringIO()
        pydidyoumean.printSuggestion('abc', ['abc', 'abcdef', 'foo'], threshold=0, includeIdenticalName=True)
        self.assertEqual(mystdout.getvalue(), 'Did you mean abc?\n')

        sys.stdout = savedStdOut


    def test_getSuggestion(self):
                # basic test
        self.assertEqual(pydidyoumean.getSuggestion('ab', ['abc', 'abcdef', 'foo']),
                         'Did you mean abc?\n')

        # test message arg
        self.assertEqual(pydidyoumean.getSuggestion('ab', ['abc', 'abcdef', 'foo'], message='How about %s?\n'),
                         'How about abc?\n')

        # test threshold arg
        self.assertEqual(pydidyoumean.getSuggestion('ab', ['abc', 'abcdef', 'foo'], threshold=0),
                         '')

        # test includeIdenticalName arg
        self.assertEqual(pydidyoumean.getSuggestion('abc', ['abc', 'abcdef', 'foo'], threshold=0, includeIdenticalName=True),
                        'Did you mean abc?\n')


    def test_suggest(self):
        # basic test
        self.assertEqual(pydidyoumean.suggest('ab', ['abc', 'abcdef', 'foo']),
                         'abc')

        # test threshold arg
        self.assertEqual(pydidyoumean.suggest('ab', ['abc', 'abcdef', 'foo'], threshold=0),
                         None)

        # test includeIdenticalName arg
        self.assertEqual(pydidyoumean.suggest('abc', ['abc', 'abcdef', 'foo'], threshold=0, includeIdenticalName=True),
                        'abc')


    def test_suggestAll(self):
        # basic test
        self.assertEqual(list(pydidyoumean.suggestAll('ab', ['abc', 'abcdef', 'foo'])),
                         ['abc'])

        # test threshold arg
        self.assertEqual(list(pydidyoumean.suggestAll('ab', ['abc', 'abcdef', 'foo'], threshold=0)),
                         [])

        # test includeIdenticalName arg
        self.assertEqual(list(pydidyoumean.suggestAll('abc', ['abc', 'abcdef', 'foo'], threshold=0, includeIdenticalName=True)),
                        ['abc'])




if __name__ == '__main__':
    unittest.main()
