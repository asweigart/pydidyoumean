import os
import sys

__version__ = '0.1.2'

runningOnPython2 = sys.version_info[0] == 2

# if SKIP_IF_OPTIMIZED is True, the printSuggestion() and printFileSuggestion()
# functions are all no-ops and do nothing when Python is run with -O
SKIP_IF_OPTIMIZED = True

'''Suggested usage:

if FILE_NOT_FOUND:
  pydidyoumean.printFileSuggestion(FILENAME) # if no suggested file is found in the cwd, this prints nothing

if COMMAND_NOT_FOUND:
  pydidyoumean.printSuggestion(CMD_NAME, LIST_OF_ALL_CMDS) # if no suggested command is found, this prints nothing

'''

def skipBecauseOptimized():
  '''If SKIP_IF_OPTIMIZED is set to True (which it is by default), then if the
  Python interpreter is being run in optimized mode (with the -O command line
  option, it determines this by checking __debug__), the   printSuggestion()
  and printFileSuggestion() functions do nothing.

  This module is really only useful for debugging while under development, but
  in production it could cause performance slow downs without providing benefit.

  Returns True if the caller should be a no-op, returns False if the caller
  should work as normal.'''
  if SKIP_IF_OPTIMIZED and not __debug__:
    return True # no-op
  else:
    return False

def printFileSuggestion(filename, message='Did you mean %s?\n', folder='.', threshold=2, includeIdenticalFilename=False):
  '''Prints the string message to display with the closest matching filename in
  the folder. Prints nothing if there are no matches within the threshold.
  Prints to sys.stdout.

  Args:
      filename (str) - The typo'd filename the user supplied.
      message (str, optional) - The format of the suggestion message to print.
        A %s conversion specifier will be replaced with the suggested name.
        Default is 'Did you mean %s?\n'
      folder (str, optional) - The folder with filenames the user could have
        meant. Default is the . current folder.
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a file from being suggested. Default is 2.
      includeIdenticalFilename (bool, optional) - If True, a filename identical
        to the filename arg will be included in the suggestions. Default is
        False.'''
  if skipBecauseOptimized(): return

  sys.stdout.write(formatFileSuggestion(filename, message, folder, threshold, includeIdenticalFilename))


def formatFileSuggestion(filename, message='Did you mean %s?\n', folder='.', threshold=2, includeIdenticalFilename=False):
  '''Returns the string message to display with the closest matching
  filename. Returns a blank string if there are no matches within the
  threshold.

  Args:
      filename (str) - The typo'd filename the user supplied.
      message (str, optional) - The format of the suggestion message to print.
        A %s conversion specifier will be replaced with the suggested name.
        Default is 'Did you mean %s?\n'
      folder (str, optional) - The folder with filenames the user could have
        meant. Default is the . current folder.
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a file from being suggested. Default is 2.
      includeIdenticalFilename (bool, optional) - If True, a filename identical
        to the filename arg will be included in the suggestions. Default is
        False.'''
  suggestedFile = suggestFile(filename, folder, threshold, includeIdenticalFilename)
  if suggestedFile is not None:
    return message % (suggestedFile)
  else:
    return ''


def suggestFile(filename, folder='.', threshold=2, includeIdenticalFilename=False):
  '''Returns the closest matching filename to the filenames in the folder. If
  there are multiple files with the same edit distance, the one returned is
  undefined. Returns None if there are no suggestions within the threshold.

  Args:
      filename (str) - The typo'd filename the user supplied.
      folder (str, optional) - The folder with filenames the user could have
        meant. Default is the . current folder.
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a file from being suggested. Default is 2.
      includeIdenticalFilename (bool, optional) - If True, a filename identical
        to the filename arg will be included in the suggestions. Default is
        False.'''
  try:
    genObj = suggestAllFiles(filename, folder, threshold, includeIdenticalFilename)
    if runningOnPython2:
      return genObj.next() # Python 2 code
    else:
      return genObj.__next__() # Python 3 code
  except StopIteration:
    return None


def suggestAllFiles(filename, folder='.', threshold=2, includeIdenticalFilename=False):
  '''Returns all suggestions in possibleSuggestions that are within the
  levenshtein edit distance of name, sorted by distance. If there are multiple
  files with the same edit distance, they will be returned in an undefined
  order.

  Args:
      filename (str) - The typo'd filename the user supplied.
      folder (str, optional) - The folder with filenames the user could have
        meant. Default is the . current folder.
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a file from being suggested. Default is 2.
      includeIdenticalFilename (bool, optional) - If True, a filename identical
        to the filename arg will be included in the suggestions. Default is
        False.'''
  filesAndDistances = [(f, levenshtein(filename, f)) for f in os.listdir(folder) if includeIdenticalFilename or f != filename]
  filesAndDistances = [x for x in filesAndDistances if x[1] <= threshold] # remove files over the threshold
  filesAndDistances.sort(key=lambda x: x[1]) # sort by comparing the levenshtein distance in x[1]

  for fd in filesAndDistances:
    yield fd[0]


def printSuggestion(name, possibleSuggestions=None, message='Did you mean %s?\n', threshold=2, includeIdenticalName=False):
  '''Prints the string message to display with the closest matching suggestion.
  Prints nothing if there are no matches within the threshold. Prints to
  sys.stdout.

  Args:
      name (str) - The typo'd name the user supplied.
      possibleSuggestions (sequence of str, optional) - A sequence of strings
        for all possible suggestions that the name could match to. This
        function will pull suggestions from this list.
      message (str, optional) - The format of the suggestion message to print.
        A %s conversion specifier will be replaced with the suggested name.
        Default is 'Did you mean %s?\n'
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a name from being suggested. Default is 2.
      includeIdenticalName (bool, optional) - If True, a name identical to
        the name  arg will be included in the suggestions. Default is False.'''
  if skipBecauseOptimized(): return

  sys.stdout.write(formatSuggestion(name, possibleSuggestions, message, threshold, includeIdenticalName))


def formatSuggestion(name, possibleSuggestions=None, message='Did you mean %s?\n', threshold=2, includeIdenticalName=False):
  '''Returns the string message to display with the closest matching
  suggestion. Returns a blank string if there are no matches within the
  threshold.

  Args:
      name (str) - The typo'd name the user supplied.
      possibleSuggestions (sequence of str, optional) - A sequence of strings
        for all possible suggestions that the name could match to. This
        function will pull suggestions from this list.
      message (str, optional) - The format of the suggestion message to print.
        A %s conversion specifier will be replaced with the suggested name.
        Default is 'Did you mean %s?\n'
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a name from being suggested. Default is 2.
      includeIdenticalName (bool, optional) - If True, a name identical to
        the name arg will be included in the suggestions. Default is False.'''
  suggestedName = suggest(name, possibleSuggestions, threshold, includeIdenticalName)
  if suggestedName is not None:
    return message % (suggestedName)
  else:
    return ''


def suggest(name, possibleSuggestions=None, threshold=2, includeIdenticalName=False):
  '''Returns the closest matching name to the suggestions in
  possibleSuggestions. Pass a list of all possible matches for the
  possibleSuggestions parameter. If there are multiple names with the same edit
  distance, the one returned is undefined. Returns None if there are no
  suggestions within the threshold.

  Args:
      name (str) - The typo'd name the user supplied.
      possibleSuggestions (sequence of str, optional) - A sequence of strings
        for all possible suggestions that the name could match to. This
        function will pull suggestions from this list.
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a name from being suggested. Default is 2.
      includeIdenticalName (bool, optional) - If True, a name identical to
        the name arg will be included in the suggestions. Default is False.'''
  try:
    genObj = suggestAll(name, possibleSuggestions, threshold, includeIdenticalName)
    if runningOnPython2:
      return genObj.next() # Python 2 code
    else:
      return genObj.__next__() # Python 3 code
  except StopIteration:
    return None


def suggestAll(name, possibleSuggestions=None, threshold=2, includeIdenticalName=False):
  '''Returns all suggestions in possibleSuggestions that are within the
  levenshtein edit distance of name, sorted by distance. If there are multiple
  names with the same edit distance, they will be returned in an undefined
  order.

  Args:
      name (str) - The typo'd name the user supplied.
      possibleSuggestions (sequence of str, optional) - A sequence of strings
        for all possible suggestions that the name could match to. This
        function will pull suggestions from this list.
      threshold (int, optional) - A levenshtein edit distance above this
        threshold will exclude a name from being suggested. Default is 2.
      includeIdenticalName (bool, optional) - If True, a name identical to
        the name arg will be included in the suggestions. Default is False.'''
  if possibleSuggestions is None:
    possibleSuggestions = []
  sugsAndDistances = [(n, levenshtein(name, n)) for n in possibleSuggestions if includeIdenticalName or n != name]
  sugsAndDistances = [x for x in sugsAndDistances if x[1] <= threshold] # remove names over the threshold
  sugsAndDistances.sort(key=lambda x: x[1]) # sort by the levenshtein distance in x[1]

  for sd in sugsAndDistances:
    yield sd[0]



def levenshtein(s1, s2):
  '''Returns the levenshtein distance (aka edit distance) between two strings.

  Args:
      s1 (str) - The first string.
      s2 (str) - The second string.'''
  # Implementation from https://code.activestate.com/recipes/576874-levenshtein-distance/
  # See also, https://en.wikipedia.org/wiki/Levenshtein_distance
  s1_length = len(s1)
  s2_length = len(s2)

  matrix = [list(range(s1_length + 1))] * (s2_length + 1)
  for zz in range(s2_length + 1):
    matrix[zz] = list(range(zz,zz + s1_length + 1))
  for zz in range(0, s2_length):
    for sz in range(0, s1_length):
      if s1[sz] == s2[zz]:
        matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
      else:
        matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
  return matrix[s2_length][s1_length]
