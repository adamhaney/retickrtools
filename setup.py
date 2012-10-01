#!/usr/bin/env python

import os
import platform

# Make sure we actually have setuptools
try:
    from setuptools import setup
except ImportError:
    if platform.linux_distribution()[0] == "Ubuntu":
        os.system("apt-get update")
        os.system("apt-get -y install python-setuptools")
        from setuptools import setup
    else:
        print "You need to install python setuptools"
        exit()


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

os.system("pip install -r requirements.txt")

setup(
    name="retickrtools",
    author="Adam Haney",
    author_email="adam.haney@retickr.com",
    version="0.1.4.9",
    description=("A collection of tools used for common idioms at retickr"),
    license="Closed",
    keywords="Data Model",
    url="http://about.retickr.com",
    packages=[
        'retickrtools',
        'retickrtools.smartrssparser'
        ],
    long_description=read('README'),
    classifiers=[
        "Topic :: Data Tools",
        "License :: OSI Approved :: Closed",
        ],
    scripts=[],
    data_files=[],
    dependency_links=[],
    install_requires=[
        ],
    zip_safe=True,
)
