import eventlet
import eventlet.timeout
from eventlet.green import urllib2


def event_network(uris, timeout=15, pool_size=1000):
    """
    Given a list of uris to pull over network pull them and then
    return a dictionary of their responses keyed on the uri which was
    originally requested
    """

    # Now, using eventlet go and fetch all of those links
    pool = eventlet.GreenPool(pool_size)

    def pull_link(link):
        try:
            with eventlet.timeout.Timeout(timeout, False):
                return (link, urllib2.urlopen(link).read())
        except:
            return (link, "")
        return (link, "")

    # Pull html for all of the links return a list of tuples in the
    # form [(link, html), ...]
    results = [
        res
        for res
        in pool.imap(pull_link, list(set(uris)))
        ]

    pool.waitall()

    return dict(filter(lambda x: type(x) != None and len(x) > 1, results))
