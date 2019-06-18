from setuptools import setup
import re

# Load version from module (without loading the whole module)
with open('pydidyoumean/__init__.py', 'r') as fo:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fo.read(), re.MULTILINE).group(1)

# Read in the README.md for the long description.
with open('README.md') as fo:
    long_description = fo.read()

setup(
    name='PyDidYouMean',
    version=version,
    url='https://github.com/asweigart/pydidyoumean',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('A module to improve "file/command not found" error messages with "did you mean" suggestions.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3+',
    packages=['pydidyoumean'],
    test_suite='tests',
    install_requires=[],
    keywords="didyoumean did you mean suggestions suggest levenshtein",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)