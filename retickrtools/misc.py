"""
misc.py conatains misc utilities that don't go in other modules.

@author: Josh Marlow
@organization: Retickr
@contact: josh.marlow@retickr.com
"""

def str2bool(str_):
    """
    Convert a string representation of a boolean value into
    an actual boolean value.

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


def deep_match(ds1, ds2):
    """
    The purpose of this function is to do a deep comparison by value between
    two data structures and indicate if they match.

    >>> deep_match(5, 5)
    True
    >>> deep_match([], [])
    True
    >>> deep_match({}, {})
    True
    >>> deep_match([0, 1, 2, 3],[0, 1, 2, 3])
    True
    >>> deep_match([0,['a', 'b', 'c'], 1, 2, 3],[0, ['a', 'b', 'c'], 1, 2, 3])
    True
    >>> deep_match({'a': 0, 'b': 1, 'c': 2}, {'a': 0, 'b' : 1, 'c': 2})
    True
    >>> deep_match({'a': 0, 'b': {'dog': 1, 'cat': 2, 'bird': 3}, 'c': 2}, {'a': 0, 'b' : {'dog': 1, 'cat': 2, 'bird': 3}, 'c': 2})
    True
    >>> deep_match(5, 3)
    False
    >>> deep_match(5, [])
    False
    >>> deep_match([], {})
    False
    >>> deep_match([0, 1, 2, 3],[0, 1, 3])
    False
    >>> deep_match([0, ['a', 'b', 'c'], 2 ,3],[0, ['a', 'c'], 1, 2, 3])
    False
    >>> deep_match({'a': 0, 'b': 1, 'c': 2}, {'a': 0, 'b' : 1, 'c': 3})
    False
    >>> deep_match({'a': 0, 'b': {'dog': 1, 'cat': 2, 'bird': 3}, 'c': 2}, {'a': 0, 'b' : {'dog': 1, 'cat': 23, 'bird': 3}, 'c': 2})
    False
    """

    # Do the types match?
    if type(ds1) != type(ds2):
        return False

    # Are they complex data types?
    if type(ds1) == list:
        # Are they the same length?
        if len(ds1) != len(ds2):
            return False

        # Do the elements match?
        for i in range(len(ds1)):
            if not deep_match(ds1[i], ds2[i]):
                return False
        else:
            # All the elements matched!
            return True
    elif type(ds1) == dict:
        # Are they the same length?
        if len(ds1) != len(ds2):
            return False

        # Do the elements match?
        for key, val in ds1.items():
            if not deep_match(val, ds2.get(key, None)):
                return False
        else:
            # All the elements matched!
            return True
    else:
        # Lets assume they simple data types
        return ds1 == ds2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
