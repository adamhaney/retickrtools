#!/usr/bin/env python2.7
"""
Retickr Pycassa

This module implements a wrapper around pycassa that attempts to convert all
incoming data into Unicode before passing it to pycassa.  To aid in this,
this module also implements smartEncodeObject, which attempts to do a
'deep conversion' of a given object to unicode.

"""

__author__ = "Josh Marlow <josh.marlow@retickr.com>"
__license__ = "Copyright (c) 2012 retickr, LLC"
__version__ = "0.1"

import pycassa

from encode_utils import smartEncodeObject


class retickrMutator:
    def __init__(self, mutator):
        self.mutator = mutator

    def insert(self, key, *args, **kwargs):
        safeKey = smartEncodeObject(key)

        self.mutator.insert(safeKey, *args, **kwargs)

    def remove(self, key, *args, **kwargs):
        safeKey = smartEncodeObject(key)

        self.mutator.remove(safeKey, *args, **kwargs)

    def send(self):
        self.mutator.send()


class retickrColumnFamily(pycassa.ColumnFamily):
    """
    This is a facade around the pycassa ColumnFamily.
    """

    def batch_insert(self, data, *args, **kwargs):
        encoding = kwargs.get("encoding", None)

        safeData = smartEncodeObject(data, encoding=encoding)

        return pycassa.ColumnFamily.batch_insert(self, safeData, *args, **kwargs)

    def batch_insert_direct(self, data, *args, **kwargs):
        """
        Bypass the normal encoding step and go straight to pycassa.
        """
        return pycassa.ColumnFamily.batch_insert(self, data, *args, **kwargs)

    def insert(self, key, data, *args, **kwargs):
        encoding = kwargs.get("encoding", None)

        safeKey = smartEncodeObject(key, encoding=encoding)
        safeData = smartEncodeObject(data, encoding=encoding)

        return pycassa.ColumnFamily.insert(self, safeKey, safeData, *args, **kwargs)

    def insert_direct(self, key, data, *args, **kwargs):
        """
        Bypass the normal encoding step and go straight to pycassa.
        """
        return pycassa.ColumnFamily.insert(self, key, data, *args, **kwargs)

    def get(self, key, *args, **kwargs):
        encoding = kwargs.get("encoding", None)

        safeKey = smartEncodeObject(key, encoding=encoding)

        return pycassa.ColumnFamily.get(self, safeKey, *args, **kwargs)

    def get_direct(self, key, *args, **kwargs):
        """
        Bypass the normal encoding step and go straight to pycassa.
        """
        return pycassa.ColumnFamily.get(self, key, *args, **kwargs)

    def multiget(self, keys, *args, **kwargs):
        encoding = kwargs.get("encoding", None)

        safeKeys = smartEncodeObject(keys, encoding=encoding)

        return pycassa.ColumnFamily.multiget(self, keys=safeKeys, *args, **kwargs)

    def multiget_direct(self, keys, *args, **kwargs):
        """
        Bypass the normal encoding step and go straight to pycassa.
        """
        return pycassa.ColumnFamily.multiget(self, keys, *args, **kwargs)

    def remove(self, key, *args, **kwargs):
        encoding = kwargs.get("encoding", None)

        safeKey = smartEncodeObject(key, encoding=encoding)

        return pycassa.ColumnFamily.remove(self, key=safeKey, *args, **kwargs)

    def remove_direct(self, key, *args, **kwargs):
        """
        Bypass the normal encoding step and go straigt hto pycassa.
        """
        encoding = kwargs.get("encoding", None)

        safeKey = smartEncodeObject(key, encoding=encoding)

        return pycassa.ColumnFamily.remove(self, keys=safeKey, *args, **kwargs)

    def ls(self):
        print "listing..."
        for (k, v) in self.cf.get_range():
            print "\t", k, v

    def purge(self):
        """
        This is basically the same as truncate, except that it
        works with the phantom node 9.
        """
        keys = [k for (k, v) in self.get_range()]

        [self.remove(k) for k in keys]

    def batch(self, *args, **kwargs):
        mutator = pycassa.ColumnFamily.batch(self, *args, **kwargs)

        return retickrMutator(mutator)


def ColumnFamily(cassandra_conn, cf_name):
    return retickrColumnFamily(cassandra_conn, cf_name)


# Alias a few pycassa modules that we didn't need to change
ConsistencyLevel = pycassa.ConsistencyLevel
NotFoundException = pycassa.NotFoundException
connect = pycassa.connect
