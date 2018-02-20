from pathlib import Path
import argparse
import logging

# Parser structure
varArgParser = argparse.ArgumentParser()
varArgParser.add_argument("--Folder", help="nothing to do here")
varArgParser.add_argument("--Debug", help="Set the level of debugging. {DEBUG|INFO|WARNING|ERROR|CRITICAL}")
varArgs = varArgParser.parse_args()

# Logging Levels
# https://docs.python.org/3/howto/logging.html#custom-levels
# The numeric values of logging levels are given in the following table.
# These are primarily of interest if you want to define your own levels, and need them to have specific
# values relative to the predefined levels. If you define a level with the same numeric value, it
# overwrites the predefined value; the predefined name is lost.
#
# Level	Numeric value
# CRITICAL	50
# ERROR	    40
# WARNING	30
# INFO	    20
# DEBUG	    10
# NOTSET	0
numeric_level = 30


# Pull the debug level if defined by the user.
varloglevel = varArgs.Debug

if varloglevel is not None:
    numeric_level = getattr(logging, varloglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % varloglevel)
logging.basicConfig(level=numeric_level)

logging.info(f"\n\nOriginal Input: {varArgs.Folder}")
logging.info(f"\n\nLast Character: {varArgs.Folder[-1]}\n\n")

# Handler for user input with appended slash at the end.
if varArgs.Folder[-1] == '"':
    varArgs.Folder = varArgs.Folder[:len(varArgs.Folder)-1]

varPath = Path(str(varArgs.Folder))

logging.info(f'After backslash handler.: varPath ={varPath}')

varThreeQuotes = "\"\"\""

if varPath:
    if Path.exists(varPath):
        for file in varPath.iterdir():
            # Skip directories inside the target path.
            if not file.is_dir():
                if str(file.absolute()).endswith(".py"):
                    print(file)
                with open(file, 'r') as f:

                    varRawFile = f.read()

                    varStartOfHeaderMultiLineComment = varRawFile.find(varThreeQuotes)
                    varEndOfHeaderMultiLineComment = varRawFile.find(varThreeQuotes, varStartOfHeaderMultiLineComment+3)

                    logging.info(f'Start: {varStartOfHeaderMultiLineComment}')
                    logging.info(f'End: {varEndOfHeaderMultiLineComment}')

                    print(varRawFile[varStartOfHeaderMultiLineComment:varEndOfHeaderMultiLineComment])
    else:
        logging.error(f'Path does not exist.: varPath ={varPath}')
