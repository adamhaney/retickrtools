"""
Returns the module path and is more robust than __file__
This tool helps with complex 'print statement debugging'

Typical Usage:

from retickrtools import module_path

def main():
    # Do stuff here

global __modpath__
__modpath__ = module_path(main)

"""

import os, inspect

def module_path(local_function):
    return os.path.abspath(inspect.getsourcefile(local_function))
