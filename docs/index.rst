.. PyDidYouMean documentation master file, created by
   sphinx-quickstart on Wed Jul  1 11:18:14 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyDidYouMean's documentation!
========================================


Installation
------------

PyDidYouMean can be installed using `pip`:

    pip install pydidyoumean

The module is available on `PyPI <https://pypi.python.org/pypi/PyDidYouMean>`__ and `GitHub <https://github.com/asweigart/pydidyoumean>`__

The documentation is available on `ReadTheDocs <http://pydidyoumean.readthedocs.org>`__

Typical Usage for "File not found" Errors
-----------------------------------------

If your code is unable to find a filename in the current working directory, you can print a "Did you mean %s?\n" message by calling:

.. code:: python

    >>> import pydidyoumean
    >>> pydidyoumean.printFileSuggestion('typo_filename.txt')

The default arguments for `printFileSuggestion()` are as follows:

.. code:: python

    >>> import pydidyoumean
    >>> pydidyoumean.printFileSuggestion('typo_filename.txt', message='Did you mean %s?\n', folder='.', threshold=2, includeIdenticalFilename=False)

The `%s` in the `message` will be replaced by the suggested file. The `threshold` is the max `Levenshtein edit distance <https://en.wikipedia.org/wiki/Levenshtein_distance>`__ (the number of character additions, removals, or replacements needed to convert one string into another). The `printFileSuggestion()` function compares the typo filename against all files and folders in `folder`. If there are multiple filenames tied for the lowest edit distance, it is undefined which one is returned.

You can get the string that `printFileSuggestion()` prints by calling `formatFileSuggestion()`, which has all the same arguments:

.. code:: python

    >>> import pydidyoumean
    >>> pydidyoumean.getFileSuggestion('typo_filename.txt')
    Did you mean typo_filename.exe?

(This naming is similar to the `pprint` module's `pprint()` and `pformat()` conventions.)

`suggestFile()` will return a string of the filename that `formatFileSuggestion()` would use, rather than an error message string. It does not have a `message` parameter.

`suggestAllFiles()` will return a generator object of all filenames that are within the threshold, sorted by distance. It does not have a `message` parameter. Pass this generator object to the `list()` function to get this as a list.


Typical Usage for "Commmand not found" Errors
---------------------------------------------

Rather than files, if your user has entered a typo'd command (or some other plain text), you can use the `printSuggestion()` function (analogous to the `printFileSuggestion()`). Instead of a `folder` parameter, `printSuggestion()` requires you pass a sequence of strings of all the possible commands that the user might have meant. The rest of the keywords are the same as `printFileSuggestion()`.

Example:

.. code:: python

    >>> import pydidyoumean
    >>> pydidyoumean.printSuggestion('checkoout', ['add', 'bisect', 'branch', 'checkout', 'clone', 'commit'])
    Did you mean checkout?

There are also functions `formatSuggestion()` (like `formatFileSuggestion()`), `suggest()` (like `suggestFile()`), and `suggestAll()` (like `suggestAllFiles()`)

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

