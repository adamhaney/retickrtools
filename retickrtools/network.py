import eventlet
import urllib2 as urllib

from retickrdata.jit.retickrurllib import urllib2

def event_network(uris):
    """
    Given a list of uris to pull over network pull them and then return a dictionary
    of their responses keyed on the uri which was originally requested
    """

    # Now, using eventlet go and fetch all of those links
    pool = eventlet.GreenPool(1000)

    def pull_link(link):
        try:
            tup = (link, urllib2.urlopen(link).read())
            return tup

        except urllib2lib.HTTPError, e:
            return (link, "")

        except Exception:
            return (link, "")

    # Pull html for all of the links return a list of tuples in the
    # form [(link, html), ...]
    results = [res for res in pool.imap(pull_link, list(set(links)))]

    pool.waitall()

    return dict(results)
