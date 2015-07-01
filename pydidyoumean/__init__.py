import os, sys

'''Suggested usage:

if FILE_NOT_FOUND:
  pydidyoumean.printSuggestion(FILENAME) # if no suggested file is found, this prints nothing
'''

def printFileSuggestion(filename, message='Did you mean %s?\n', folder='.', threshold=2, includeIdenticalFilename=False):
  sys.stdout.write(getFileSuggestion(filename, message, folder, threshold, includeIdenticalFilename))


def getFileSuggestion(filename, message='Did you mean %s?\n', folder='.', threshold=2, includeIdenticalFilename=False):
  suggestedFile = suggestFile(filename, folder, threshold, includeIdenticalFilename)
  if suggestedFile is not None:
    return message % (suggestedFile)
  else:
    return ''


def suggestFile(filename, folder='.', threshold=2, includeIdenticalFilename=False):
  '''Returns the first'''
  try:
    return suggestAllFiles(filename, folder, threshold, includeIdenticalFilename).__next__()
  except StopIteration:
    return None


def suggestAllFiles(filename, folder='.', threshold=2, includeIdenticalFilename=False):
  '''Returns the first. If there are multiple files with the same edit distance, they will be returned in an undefined order.'''
  filesAndDistances = [(f, levenshtein(filename, f)) for f in os.listdir(folder) if includeIdenticalFilename or f != filename]
  filesAndDistances = [x for x in filesAndDistances if x[1] <= threshold] # remove files over the threshold
  filesAndDistances.sort(key=lambda x: x[1]) # sort by comparing the levenshtein distance in x[1]

  for fd in filesAndDistances:
    yield fd[0]


def printSuggestion(name, message='Did you mean %s?\n', possibleSuggestions=None, threshold=2, includeIdenticalFilename=False):
  pass


def getSuggestion(filename, message='Did you mean %s?\n', possibleSuggestions=None, threshold=2, includeIdenticalFilename=False):
  pass


def suggest(filename, possibleSuggestions=None, threshold=2, includeIdenticalFilename=False):
  pass


def suggestAll(filename, possibleSuggestions=[], threshold=2, includeIdenticalFilename=False):
  pass



def levenshtein(s1, s2):
  '''Returns the levenshtein distance (aka edit distance) between two strings.'''
  # Implementation from https://code.activestate.com/recipes/576874-levenshtein-distance/
  # See also, https://en.wikipedia.org/wiki/Levenshtein_distance
  s1_length = len(s1)
  s2_length = len(s2)

  matrix = [list(range(s1_length + 1))] * (s2_length + 1)
  for zz in range(s2_length + 1):
    matrix[zz] = list(range(zz,zz + s1_length + 1))
  for zz in range(0,s2_length):
    for sz in range(0,s1_length):
      if s1[sz] == s2[zz]:
        matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
      else:
        matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
  return matrix[s2_length][s1_length]
