#!/usr/bin/env python

import StringIO
import tarfile

import simplejson
import simplejson.decoder

def untar_feed_objs(_buffer):
    """
    We commonly tar a collection of feed objects to reduce the number
    of files we're dealing with. This method takes a tar file as a
    buffer and generates a list of feed objects from it
    """
    tar = tarfile.TarFile.open(fileobj=StringIO.StringIO(_buffer.read()))
    for member in tar.getmembers()[:1]:
        yield simplejson.loads(tar.extractfile(member).read())


def kv_line_read(line, wtf_function=lambda e: 'NULL'):
    """
    Takes a line from a TSV file and replaces the html newlines and
    restores them returning the key value pair as a tuple. If the value
    was a SIMPLEJSON object it returns it as a Python object of that type.

    NOTE: This module doesn't take any crap from you or your friends.
    It won't throw exceptions, it'll handle business. If you give it
    a line that it can't read it'll return the `wtf_string` so we can
    keep going. 
    
    """

    def restore_bad(str_):
        return str_.replace("&#09;", "\t").replace("&#10", "\n")

    split_line = line.split('\t')

    try:
        key = restore_bad(split_line[0])
        value = simplejson.loads(restore_bad(split_line[1]))

    except (IndexError, simplejson.decoder.JSONDecodeError), e:
        return wtf_function(e, str_)

    return (key, value)


def kv_line_write(key, value):
    """
    Takes a key and value replaces the tabs and newline characters with
    html entities and then returns a tab seperated string. If the value
    is a python object it SIMPLEJSON encodes it.
    """

    def escape_bad(str_):
        return str_.replace("\t", "&#09;").replace("\n", "&#10")

    return "{0}\t{1}\n".format(
        escape_bad(key),
        escape_bad(simplejson.dumps(value)))

def load_kv(tsv_buffer):
    """
    This function takes a TSV object file as an argument and returns a
    dictionary of key value mappings
    """
    tsv_obj = {}
    for line in tsv_buffer.read().split("\n"):
        k, v = kv_line_read(line)
        tsv_obj[k] = v

    return tsv_obj
        

class ReadFailed(Exception):
    pass


class WriteFailed(Exception):
    pass
