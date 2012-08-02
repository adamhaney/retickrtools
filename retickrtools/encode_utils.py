#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Note: the above coding directive is only so that we can include unicode
# literals in actual Python source
from collections import OrderedDict
import re


def smartDecodeObject(obj, encoding=None):
    """
    Given an object which has been processed by smartEncodeObject
    convert it (and any objects contained therein) back to it's former
    unicode glory.  What this means is expanding any xml character references
    back into the their full and righteous unicode code points.
    """
    def ascii2unicode(str_ascii):
        def xmlcharref2chr(matchObj):
            return chr(int(matchObj.group(0)[2:-1]))
        def xmlcharref2unichr(matchObj):
            return unichr(int(matchObj.group(0)[2:-1]))

        try:
            str_utf8 = re.sub('&#\d+;', xmlcharref2chr, str_ascii)

            return unicode(str_utf8, "utf-8")
        except ValueError:
            return re.sub('&#\d+;', xmlcharref2unichr, str_ascii)

    return __smartConvertObject(obj, ascii2unicode, ascii2unicode)


def smartEncodeObject(obj, encoding=None):
    """
    Given an object which may contain unicode, convert it
    (and any objects contained therein) such that the unicode
    is replaced with ascii and the non-ascii code points (>128)
    are converted to xml character references.  So the object
    will be pure ascii.
    """
    asciiErrorsPolicy = "xmlcharrefreplace"

    def unicode2ascii(uniData):
        return uniData.encode("ascii", errors=asciiErrorsPolicy)

    def smartEncodeString(data):
        """
        Attempt to convert the data to unicode using various encoding schemes
        """
        return unicode2ascii(data.decode("unicode_escape"))

    return __smartConvertObject(obj, smartEncodeString, unicode2ascii)


def __smartConvertObject(obj, stringConvertFunction, unicodeConvertFunction):
    """
    Attempt to do a deep conversion of the object, obj, in some way.
    That's an awfully nebulous description, but this function is really just
    meant as a skeleton.  Strings are processed using the stringConvertFunction,
    unicode objects are processed using the unicodeConvertFunction.
    Any kind of composite objects (lists, dictionaries,
    etc) are recursively converted.

    """
    if isinstance(obj, str):
        return stringConvertFunction(obj)

    elif isinstance(obj, OrderedDict):
        # Note: we cannot use a normal dictionary comprehension below,
        # because that creates an *unordered dictionary* before
        # creating an OrderedDict and that blows away the ordering information
        return OrderedDict([(__smartConvertObject(k, stringConvertFunction,
                                                unicodeConvertFunction),
                              __smartConvertObject(v, stringConvertFunction,
                                                 unicodeConvertFunction))
                              for k, v in obj.items()])
    elif isinstance(obj, dict):
        return {__smartConvertObject(k, stringConvertFunction,
                                   unicodeConvertFunction):
                __smartConvertObject(v, stringConvertFunction,
                                   unicodeConvertFunction)
                    for k, v in obj.items()}
    elif isinstance(obj, list):
        return [__smartConvertObject(e, stringConvertFunction,
                                   unicodeConvertFunction)
                    for e in obj]
    elif isinstance(obj, tuple):
        return tuple([__smartConvertObject(e, stringConvertFunction,
                                         unicodeConvertFunction)
                    for e in obj])
    elif isinstance(obj, unicode):
        return unicodeConvertFunction(obj)

    return obj


if __name__ == "__main__":
    print smartDecodeObject("Do&#197;&#130;ek dla nauczycieli")
    print u'Dołek dla nauczycieli'
    print smartDecodeObject("straight ascii")
    print smartDecodeObject("Stanley Kubrick&#226;&#128;&#153;s Interview with The New Yorker")
    print smartDecodeObject(u"Stanley Kubrick&#226;&#128;&#153;s Interview with The New Yorker")
