"""
url_utils.py is a module that conatains various utility
functions for dealing with URLs.

@author: Joshua Colt "young stallion" Marlow
@organization: Retickr
@contact: josh.marlow@retickr.com
"""

__author__ = "Josh Marlow"
__contact__ = "josh.marlow@retickr.com"
__license__ = "Copyright (c) 2012 retickr, LLC"

# Universe imports
import base64
import re
import urlparse


def build_source_proxy_url(service, service_username):
    """
    Given a service and a service_username, construct the source proxy
    URL for it.

    >>> build_source_proxy_url("facebook", "joshmarlow@gmail.com")
    'https://mynews.retickr.com/sources/facebook/am9zaG1hcmxvd0BnbWFpbC5jb20='
    >>> build_source_proxy_url("twitter", "JoshuaMarlow")
    'https://mynews.retickr.com/sources/twitter/Sm9zaHVhTWFybG93'
    """
    return "{0}/sources/{1}/{2}".format(
            "https://mynews.retickr.com",
            service,
            base64.b64encode(service_username))


def build_source_proxy_name(service, resource_name):
    """
    Given a service and a service_username, construct the source proxy
    name for it.

    >>> build_source_proxy_name("facebook", "joshmarlow@gmail.com")
    'facebook/am9zaG1hcmxvd0BnbWFpbC5jb20='
    >>> build_source_proxy_name("twitter", "JoshuaMarlow")
    'twitter/Sm9zaHVhTWFybG93'

    """
    return "{0}/{1}".format(service, base64.b64encode(resource_name))


def valid_source_proxy(url):
    mo = re.match(r"(facebook|twitter|feed)/(?P<resource>)", url)

    if mo:
        try:
            base64.b64decode(mo.groupdict()["resource"])
            return True
        except (KeyError, TypeError):
            return False

    return False


def valid_source_proxy_url(url):
    """
    Indicates if the provided url is a valid source proxy
    URL.

    >>> valid_source_proxy_url('https://mynews.retickr.com/sources/feed/aHR0cDovL3Jzc2ZlZWRzLnVzYXRvZGF5LmNvbS91c2F0b2RheS1OZXdzVG9wU3Rvcmllcw==')
    True
    >>> valid_source_proxy_url('http://rssfeeds.usatoday.com/usatoday-NewsTopStories')
    False
    """
    return None != extract_resource_name_from_url(url)


def extract_fields_from_source_proxy_name(source_proxy_name):
    """
    Given a source proxy name, extract the service and a service_username
    from it

    >>> extract_fields_from_source_proxy_name(\
    'facebook/am9zaG1hcmxvd0BnbWFpbC5jb20=')
    ('facebook', 'joshmarlow@gmail.com')
    >>> extract_fields_from_source_proxy_name(\
    'twitter/Sm9zaHVhTWFybG93')
    ('twitter', 'JoshuaMarlow')

    """
    delim_idx = source_proxy_name.index('/')

    service_name = source_proxy_name[:delim_idx]
    b64_resource_name = source_proxy_name[delim_idx + 1:]

    resource_name = base64.b64decode(b64_resource_name)

    return (service_name, resource_name)


def extract_resource_name_from_url(source_proxy_url):
    """
    Given a source proxy URL, extract the resource name from it.

    >>> extract_resource_name_from_url(\
    "https://mynews.retickr.com/sources/facebook/am9zaG1hcmxvd0BnbWFpbC5jb20=")
    'facebook/am9zaG1hcmxvd0BnbWFpbC5jb20='
    >>> extract_resource_name_from_url(\
    "http://www.google.com")
    >>> extract_resource_name_from_url(\
    "http://twitter.com/sources/blarg")
    """
    resource_path = urlparse.urlparse(source_proxy_url).path

    mo = re.match(r'/sources/(?P<resource_name>.+)', resource_path)

    if mo and "resource_name" in mo.groupdict().keys():
        # This is a valid resource name
        resource_name = mo.groupdict()["resource_name"]

        if valid_source_proxy(resource_name):
            return resource_name

    return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
