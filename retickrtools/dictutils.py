#!/usr/bin/env python

import retickrtools.distance_functions    

def dictdistance(
    dicta,
    dictb,
    distance_function=retickrtools.distance_functions.euclidean):
    """
    This function takes two dictionaries which match the form

    >>> a = {"keya": 0.27, "keyb": 0.32} 
    >>> b = {"keyb": 0.44, "keyc": 0.72}

    It assumes that each key represents a particular dimension and that
    this dictionaries themselve are actually dense representations of a
    sparse matrix in a highly dimensioned space. Because of this,
    if a key is missing from one dictionary that value is assumed to be 
    zero. The function returns a tuple where the first element is the
    distance and the second element is the ratio of overlapping elements
    to nonoverlapping elements (for exactly matching dictionaries this
    value will be 1).
    """
    
    overlapping_values = [
        (dicta[key], dictb[key])
        for key
        set(dicta) & set(dictb)
        ]

    disjoint_values = [
        (dicta[key], 0)
        for key
        in set(dicta) - set(dictb)
        ]

    disjoint_values += [
        (dictb[key], 0)
        for key
        in set(dictb) - set(dicta)
        ]
        
    overlap = 1

    if disjoint_values > 0:
        overlap = len(overlapping_values) / len(disjoint_values) 

    # Convert list of tuples that were in the form (x1, x2), (y1, y2)
    # Into two 'proper' points (x1, y1), (x2, y2)
    point_dict = dict(overlapping_values, disjoin_values)
    pointa = point_dict.keys()
    pointb = point_dict.values()

    return distance_function(pointa, pointb), overlap
