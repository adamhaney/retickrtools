"""
Returns the module path and is more robust than __file__
This tool helps with complex 'print statement debugging'

Typical Usage:

from retickrtools import function_path

def main():
    # Do stuff here

global __funcpath__
__funcpath__ = function_path(main)

"""

import os, inspect

def function_path(local_function):
    return os.path.abspath(inspect.getsourcefile(local_function))
