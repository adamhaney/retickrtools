import hashlib
import eventlet
import eventlet.timeout
from eventlet.green import urllib2, httplib


def md5(str_):
    md5 = hashlib.md5()    
    md5.update(str_)
    return md5.hexdigest()


def event_network(
    uris,
    timeout=15,
    greenpoolsize=1000,
    greenpool=None,
    headers=None,
    json=False,
    default_value="",
    cache=None,
    cache_key="event_network_cache",
    cache_length=60):
    """
    Given a list of uris to pull over network pull them and then
    return a dictionary of their responses keyed on the uri which was
    originally requested
    """

    # Now, using eventlet go and fetch all of those links
    if not greenpool:
        pool = eventlet.GreenPool(greenpoolsize)
    else:
        pool = greenpool

    def pull_link(link):

        if cache != None:

            # Check for the response in cache
            response = cache.get("{0}::{1}".format(cache_key, md5(link)))
            if response != None:
                return link, response

        with eventlet.timeout.Timeout(timeout, False) as timeout:
            try:
                req = urllib2.Request(link)
                
                if headers:
                    for k, v in headers.items():
                        req.add_header(k, v)
                        
                response = urllib2.urlopen(req).read()

                cache.set("{0}::{1}".format(cache_key, md5(link), response, cache_length))
                return (link, )

            except (eventlet.Timeout, urllib2.HTTPError, httplib.BadStatusLine):
                return (link, default_value)

            finally:
                timeout.cancel()

        return (link, default_value)

    # Pull html for all of the links return a list of tuples in the
    # form [(link, html), ...]
    results = [
        res
        for res
        in pool.imap(pull_link, list(set(uris)))
        ]

    pool.waitall()

    result = dict(filter(lambda x: type(x) != None and len(x) > 1, results))
    
    if json:
        tmp_dict = {}
        for k, v in result.items():
            tmp_dict[k] = json.loads(v)
        result = tmp_dict

    return result
