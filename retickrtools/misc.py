"""
misc.py conatains misc utilities that don't go in other modules.

@author: Josh Marlow
@organization: Retickr
@contact: josh.marlow@retickr.com
"""

def cast_to_bool(str_):
    str_ = str_.strip().lower()

    if "true" == str_:
        return True
    elif "false" == str_:
        return False
