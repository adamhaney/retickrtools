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

# Retickr imports
import retickrtools.constants as rtkr_constants

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


def valid_source_proxy_name(url):
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

        if valid_source_proxy_name(resource_name):
            return resource_name

    return None


def url_is_retickr_redirect(url):
    """
    This function takes a given url and returns true of false
    if it is a url that points to a retickr story
    """
    if url.find(rtkr_constants.redirect_url) != -1:
        return True
    return False


def redirect2id(url):
    """
    This function takes a retickr redirect url and returns
    the story_id it is associated with. If you pass
    in a url that isn't a valid redirect url we raise a
    type error

    :Parameters:
      url : string
        A string representing the url we want to convert to an id

    >>> redirect2id("{0}/58e3d260".format(rtkr_constants.redirect_url))
    '58e3d260'

    """

    url = url.strip()
    if not url_is_retickr_redirect(url):
        raise TypeError("{0} is not a redirect url".format(url))

    id_ = url.replace(rtkr_constants.redirect_url, "").replace("/", "")

    return id_


def __make_valid_resource(str_, validator):
    """
    We often want to check if a particular string is
    a valid URL (for some definition of valid).  For instance,
    we might want to check if a given string is a valid
    URL, a valid feed URL, etc.

    This is a quick skeleton function that accepts a
    string and a validator function and calls the
    validator with the string as an argument.
    It thus determins if the provided
    string is valid (according to the validator function).

    Finally, it makes sure that there is a protocol
    prefixing that URL.

    """
    url = None

    if reject_as_hopeless_url(str_):
        return None

    # Make sure the q is a valid URL
    if not validator(str_):
        return None

    # Make sure we have a protocol
    if get_protocol(str_):
        # The URL already has a protocol
        url = str_
    else:
        url = "http://" + str_

    return url

def reject_as_hopeless_url(str_):
    """
    Various substrings can cause exceptions from withint urllib2
    Here we look for some of those substrings and reject the URL out of hand if
    we find them

    >>> reject_as_hopeless_url("http://mynews.retickr.com/user/josh.marlow@retickr.com/management")
    False
    >>> reject_as_hopeless_url("http:/slashdot.org/rss/current.xml")
    True
    >>> reject_as_hopeless_url("http://slashdot:bob.org/rss/current.xml")
    True
    """
    if re.search(r":/(?!/)", str_):
        # Butchered protocol
        return True
    if re.search(r":(?![\d/])", str_):
        # Random ':' in the middle of text
        return True

    return False


def valid_url(str_, requireProtocol=False):
    """
    Given a string, return true if it appears to be a valid url.

    >>> valid_url('http://reddit.com/.rss')
    True
    >>> valid_url('http://wwww.reddit.com/.rss')
    True
    >>> valid_url('https://wwww.reddit.com/.rss')
    True
    >>> valid_url('wwww.reddit.com/.rss')
    True
    >>> valid_url('wwww.reddit.com/.rss', False)
    True
    >>> valid_url('wwww.reddit.com/.rss', True)
    False
    >>> valid_url('(null)')
    False
    >>> valid_url('feed://www.reddit.com/.rss', True)
    False
    """

    if reject_as_hopeless_url(str_):
        return False

    acceptableProtocolList = ["http", "https"]

    if requireProtocol:
        mo = re.match(r"((?P<protocol>.+)://).+\..+", str_)

        return (
            (None != mo)
            and (mo.groupdict()["protocol"] in acceptableProtocolList))
    else:
        return None != re.match(r".+\..+", str_)


def valid_feed_url(str_, requireProtocol=False):
    """
    Currently, the valid_feed_url works just like the
    general valid_urlfunction eventually.  Eventually,
    we may add additional constraints for checking that
    a URL is also a feed URL.
    For now we are just making it a facade
    around the valid_url function.
    """
    return valid_url(str_, requireProtocol)


def get_protocol(url):
    """
    Given a url, extract it's protocol

    >>> get_protocol("http://www.retickr.com")
    'http'
    >>> get_protocol("https://www.retickr.com")
    'https'
    >>> get_protocol("ftp://www.retickr.com")
    'ftp'
    >>> get_protocol("www.retickr.com")
    """

    mo = re.match(r"(?P<protocol>.+)://.+", url)

    if mo:
        return mo.groupdict()["protocol"]
    else:
        return None


def is_valid_feed(str_):
    """
    Returns a bool indicating if the provided str_ is
    either valid RSS or Atom or not.

    TODO: We will eventually want to be more precise and stringent concerning
    what we consider to be valid feeds.  See #567 for a discussion.

    >>> is_valid_feed("<rss></rss>")
    True
    >>> is_valid_feed("<Rss></Rss>")
    True
    >>> is_valid_feed("<RSS></RSS>")
    True
    >>> is_valid_feed("<atom></atom>")
    True
    >>> is_valid_feed("I still like tacos")
    False
    >>> is_valid_feed("<html></html>")
    False
    >>> is_valid_feed('<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" version="2.0"></rss>')
    True
    >>> is_valid_feed('<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" version="2.0">\\n</rss>')
    True
    """
    rssMo = re.search(r"<rss.*>.*</rss>", str_, re.IGNORECASE | re.DOTALL)

    if rssMo:
        return True

    atomMo = re.search(r"<atom.*>.*</atom>", str_, re.IGNORECASE | re.DOTALL)

    if atomMo:
        return True

    return False


def make_valid_url(str_):
    """
    >>> make_valid_url("static.retickr.com/testing/rss/reddit.rss")
    'http://static.retickr.com/testing/rss/reddit.rss'
    >>> make_valid_url("http://static.retickr.com/testing/rss/reddit.rss")
    'http://static.retickr.com/testing/rss/reddit.rss'
    >>> make_valid_url("foobar")
    """
    return __make_valid_resource(str_, valid_url)


def make_valid_feed_url(str_):
    """
    >>> make_valid_feed_url("static.retickr.com/testing/rss/reddit.rss")
    'http://static.retickr.com/testing/rss/reddit.rss'
    >>> make_valid_feed_url("http://static.retickr.com/testing/rss/reddit.rss")
    'http://static.retickr.com/testing/rss/reddit.rss'
    >>> make_valid_feed_url("foobar")
    """
    return __make_valid_resource(str_, valid_feed_url)


def url2sitename(url):
    """
    Given a hostname of the form (www.sitename.tld)
    strip out the www. and the tld and return the sitename

    >>> url2sitename("www.retickr.com")
    'retickr'
    >>> url2sitename("retickr.com")
    'retickr'
    >>> url2sitename("dev.retickr.com")
    'dev.retickr'
    >>> url2sitename("www.dev.retickr.ht")
    'dev.retickr'
    >>> url2sitename("www.awww.com")
    'awww'
    >>> url2sitename("http://www.retickr.com")
    'retickr'
    >>> url2sitename("http://mynews.retickr.com/sources/feed/aHR0cHM6Ly90d2l0dGVyLmNvbS9zdGF0dXNlcy91c2VyX3RpbWVsaW5lLzEzMzQ4LnJzcw==")
    'twitter'
    """

    url = url.strip()

    # Check if this is a source proxy URL
    resource_name = url_utils.extract_resource_name_from_url(url)

    if resource_name:
        url = url_utils.extract_fields_from_source_proxy_name(resource_name)[1]

    # Massage the data a bit; urlparse needs it to have a protocol...
    if None == get_protocol(url):
        url = "http://" + url

    # Finally we've got a URL to check
    hostname = urlparse.urlparse(url).hostname

    if hostname:
        mo = re.match(
            r"(?P<www>www\.)?(?P<sitename>.+)\.(?P<tld>.+)",
            hostname
            )

        if mo:
            return mo.groupdict()["sitename"]
        else:
            return hostname

    return url


if __name__ == "__main__":
    import doctest

    doctest.testmod()
