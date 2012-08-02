"""
misc.py conatains misc utilities that don't go in other modules.

@author: Josh Marlow
@organization: Retickr
@contact: josh.marlow@retickr.com
"""

def str2bool(str_):
    """
    >>> str2bool('False')
    False
    >>> str2bool('false')
    False
    >>> str2bool('True')
    True
    >>> str2bool('true')
    True
    """
    str_ = str_.strip().lower()

    if "true" == str_:
        return True
    elif "false" == str_:
        return False

if __name__ == "__main__":
    import doctest

    doctest.testmod()
