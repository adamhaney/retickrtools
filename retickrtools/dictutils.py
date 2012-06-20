#!/usr/bin/env python

import UserDict
import collections


def dict_sparse_points(dicta, dictb):
    """
    This function takes two dictionaries and creates a sparse vector
    of their overlapping and disjoint values to create two vectors
    that are in the same "space"

    >>> a = {"a": 1, "b": 2}
    >>> c = {"c": 3, "d": 4}
    >>> dict_sparse_points(a, c)
    ((1, 0.0, 2, 0.0), (0.0, 3, 0.0, 4))
    """

    all_keys = list(set(dicta.keys() + dictb.keys()))

    return (
        # Point A
        tuple(
            dicta.get(k, 0.0)
            for k
            in all_keys
            ),

        # Point B
        tuple(
            dictb.get(k, 0.0)
            for k
            in all_keys
            )
        )


def dict_distance(
    dicta,
    dictb,
    distance_function):
    """
    This function takes two dictionaries which match the form

    >>> a = {"keya": 0.27, "keyb": 0.32, "keyc": 0.74, "keyd": 0.27}
    >>> b = {"keyb": 0.44, "keyc": 0.72}
    >>> dictdistance(a, b)

    It assumes that each key represents a particular dimension and
    that this dictionaries themselve are actually dense
    representations of a sparse matrix in a highly dimensioned
    space. Because of this, if a key is missing from one dictionary
    that value is assumed to be zero. The function returns a tuple
    where the first element is the distance and the second element is
    the ratio of overlapping elements to nonoverlapping elements (for
    exactly matching dictionaries this value will be 1).
    """

    points, overlap = dict_sparse_points(dicta, dictb)

    return distance_function(points[0], points[1]), overlap


if "__main__" == __name__:
    import doctest

    extraglobs = {}

    print doctest.testmod(extraglobs=extraglobs)


class DistanceDictionary(UserDict.UserDict):
    """
    This is an object that allows us to only store one scalar
    distance value for a pair of points but it checks the points
    in both directions if it can't find it in one place (since we
    know they're the same). Also, for convenience if you're
    finding the distance between two points that are the same
    place it returns 0.
    """

    def __getitem__(self, key):
        """
        >>> d = DistanceDictionary({'a': 'b'})
        >>> d.keys()
        ['a']

        >>> d['a']
        'b'

        >>> d = DistanceDictionary({(1, 2): 7})
        >>> d[(1, 2)]
        7

        >>> d[(2, 1)]
        7

        # You can also call tuple keys without using paranthesis
        >>> d[2, 1]
        7

        """
        try:
            return self.data[key]

        except KeyError:
            if key[0] != key[1]:
                try:
                    return self.data[(key[1], key[0])]
                except KeyError:
                    raise KeyError(key)
            else:
                return 0


class HashableDictionary(UserDict.UserDict):
    """
    Sometimes we want to treat dictionaries that have words and
    floating point value as tuples. This is very similar to a named
    tuple. But the interface to a named tuple is a bit different than
    that of a dictionary. But, you can't hash dictionaries. This
    dictionary allows us to hash the JSON representation of itself so
    we can use the "dictionary" itself as a hashable key.
    """

    def __hash__(self):
        """
        This method adds a __hash__ function to a dictionary element
        which hashes the dictionary's JSON representation. This
        obviously only works for dictionaries that can be JSON
        serialized.

        >>> dict_ = HashableDict
        """
        return hash(collections.FrozenSet(self.data.items()))
