"""
This script performs common matrix operations. It assumes that we will pass
in matrices as lists of lists. Functions internal to this module may then
(but aren't guaranteed) to convert them into numpy arrays, but the output
should still be returned in terms of lists of lists
"""


def sum_columns(matrix):
    """
    For a list of lists such as return the sum of the columns as a list.

    >>> matrix = [[1, 2, 3, 4],
    ...           [5, 6, 7, 8]]

    >>> sum_columns(matrix)
    [6, 8, 10, 12]

    We assume that all the lists have the same number of elements
    and that they are of the same type. Although, any type which
    supports the "+" operator may use this function (including
    'strange' cases, such as strings.

    """

    column_sum = []

    # Initialize the column sum by appending all the elements in the
    # first row to it.
    for row in matrix:
        for column in row:
            column_sum.append(0)
        break

    for row in matrix:
        for ii, column in enumerate(row):
            column_sum[ii] = column_sum[ii] + column

    return column_sum


def unit_vector(vector):
    """
    For a given vector return its unit vector. In our case we assume
    that a vector is a list of numbers. It returns a list of floats
    that represent the unit vector

    >>> unit_vector([1, 1, 2, 0])
    [0.25, 0.25, 0.5, 0.0]

    """

    sum_vector = sum(vector)
    return [float(elm) / sum_vector for elm in vector]

if __name__ == "__main__":
    import doctest

    extraglobs = {}

    print doctest.testmod(extraglobs=extraglobs)
