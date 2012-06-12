"""
Often times in life, and data mining, you would like to know the distance
between two points. There are many many different functions that will
provide this information for us. This module aims to include them
so that when you're writing code you don't have to implement these
distance functions yourself
"""

import math

from dictutils import DistanceDictionary

def squared_euclidean(pointa, pointb):
    """
    The same as euclidean distance except we don't
    scale this function by square rooting the
    sum of the squared point differences
    
    >>> squared_euclidean((0, 0), (1, 1))
    2

    """
    assert len(pointa) == len(pointb)

    return sum(
            [
                (dimension[0] - dimension[1]) ** 2
                for dimension
                in zip(pointa, pointb)
                ]
            )

def euclidean(pointa, pointb):
    """
    Takes two points and returns the euclidean
    distance between them

    >>> euclidean((0, 0), (1, 1))
    1.4142135623730951

    """

    return math.sqrt(squared_euclidean(pointa, pointb))

def hamming(pointa, pointb):
    """
    The hamming distance between two strings is the
    number of positions at which coresponding symbols are different
    http://en.wikipedia.org/wiki/Hamming_distance

    >>> hamming((0, 1, 2, 3), (0, 1, 0, 0))
    2
    
    """

    assert len(pointa) == len(pointb)

    return sum(dimension[0] != dimension[1] for dimension in zip(pointa, pointb))


def pairwise_distances(iterable_points, distance_function):
    """
    Given an iterable and a distance function that can take two points
    from that iterable return a dictionary that maps pointa to pointb
    and pointb to pointa (without doing the computation twice)

    >>> points = [(1, 1), (2, 2), (3, 3)]

    >>> distances = pairwise_distances(points, euclidean)
    >>> distances[(1, 1), (3, 3)]
    2.8284271247461903

    >>> distances[(3, 3), (1, 1)]
    2.8284271247461903

    >>> distances[(2, 2), (3, 3)]
    1.4142135623730951

    Computation Reduction
    ---------------------

    Pairwise computation for a large number of points has a very bad
    computatoin footprint with the naive approach (O(n**2)). So we do
    a few things to reduce the computation. First it should noted that
    the distance from a to b is the same as the distance from b to
    a. So we only do the computation once (we pass back an object that
    knows to look in both places for the value though so we have a
    simplified interface that doesn't have an increased memory
    footprint).

    We can think of these computations as a matrix where the rows and
    columns are a coordinates which represent the distance between two
    points (and in which direction).

    A    B    C    D
    
    B    0
    
    C         0
    
    D              0

    The distance from a to a, b to b, etc is always 0 so we can skip
    this computation, and our DistanceDictionary class knows this.

    """

    distance_tuples = []

    for ii in range(len(iterable_points)):

        distance_tuples += [
            (
                (
                    iterable_points[ii],
                    iterable_points[jj]
                    ),
                distance_function(iterable_points[ii], iterable_points[jj])
                )
            for jj
            in range(0, ii)
            ]

    distance_dictionary = DistanceDictionary(distance_tuples)
    return distance_dictionary

  
if "__main__" == __name__:
    import doctest
    
    extraglobs = {}

    print doctest.testmod(extraglobs=extraglobs)
