# PyDidYouMean

A module to improve "file/command not found" error messages with "did you mean" suggestions.

Install with:

    pip install pydidyoumean

Typical usage:

    if FILE_NOT_FOUND:
      pydidyoumean.printFileSuggestion(FILENAME) # if no suggested file is found in the cwd, this prints nothing
      # prints out "Did you mean %s?\n" % (SUGGESTED_FILENAME)

    if COMMAND_NOT_FOUND:
      pydidyoumean.printSuggestion(CMD_NAME, LIST_OF_ALL_CMDS) # if no suggested command is found, this prints nothing
      # prints out "Did you mean %s?\n" % (SUGGESTED_CMD)

There are several other functions and optional parameters for customizing the message or getting the recommendations. Docs are at https://pydidyoumean.readthedocs.org

Support
-------

If you find this project helpful and would like to support its development, [consider donating to its creator on Patreon](https://www.patreon.com/AlSweigart).
