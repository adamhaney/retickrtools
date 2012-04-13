#!/usr/bin/env python

import StringIO
import tarfile

try:
    import simplejson as json
except ImportError:
    import json


def untar_feed_objs(_buffer):
    """
    We commonly tar a collection of feed objects to reduce the number
o    of files we're dealing with. This method takes a tar file as a
    buffer and generates a list of feed objects from it
    """
    tar = tarfile.TarFile.open(fileobj=StringIO.StringIO(_buffer.read()))
    for member in tar.getmembers()[:1]:
        yield json.loads(tar.extractfile(member).read())

def kv_line_read(line):
    """
    Takes a line from a TSV file and replaces the html newlines and
    restores them returning the key value pair as a tuple. If the value
    was a JSON object it returns it as a Python object of that type.
    """

    def restore_bad(str_):
        return str_.replace("&#09;", "\t").replace("&#10", "\n")

    return (restore_bad(line.split('\t')[0]), json.loads(restore_bad(line.split('\t')[1])))


def kv_line_write(key, value):
    """
    Takes a key and value replaces the tabs and newline characters with
    html entities and then returns a tab seperated string. If the value
    is a python object it JSON encodes it.
    """

    def escape_bad(str_):
        return str_.replace("\t", "&#09;").replace("\n", "&#10")

    return "{0}\t{1}\n".format(escape_bad(key), escape_bad(json.dumps(value)))
        
