"""
Often times in life, and data mining, you would like to know the distance
between two points. There are many many different functions that will
provide this information for us. This module aims to include them
so that when you're writing code you don't have to implement these
distance functions yourself
"""

import math

def squared_euclidean(pointa, pointb):
    """
    The same as euclidean distance except we don't
    scale this function by square rooting the
    sum of the squared point differences
    """
    assert len(pointa) == len(pointb)

    return sum(
            [
                dimension[0] - dimension[1] ** 2
                for dimension
                in zip(pointa, pointb)
                ]
            )

def euclidean(pointa, pointb):
    """
    Takes two points and returns the euclidean
    distance between them
    """

    return math.sqrt(squared_euclidean_distance(pointa, pointb))

def hamming(pointa, pointb):
    """
    The hamming distance between two strings is the
    number of positions at which coresponding symbols are different
    http://en.wikipedia.org/wiki/Hamming_distance
    """

    assert len(pointa) == len(pointb)

    return sum(dimension[0] != dimension[1] for dimension in zip(pointa, pointb))

