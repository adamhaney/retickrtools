# Universe imports
import json

# Thirdparty imports
import eventlet
import eventlet.timeout
from eventlet.green import urllib2, httplib


def event_network(uris, timeout=15, greenpoolsize=1000, greenpool=None,
    headers=None, treat_results_as_json=False, default_value="",
    filter_out_empty_responses=True):
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
        with eventlet.timeout.Timeout(timeout, False) as timeout_obj:
            try:
                req = urllib2.Request(link)

                if headers:
                    for k, v in headers.items():
                        req.add_header(k, v)

                return (link, urllib2.urlopen(req).read())

            except (eventlet.Timeout, urllib2.HTTPError, httplib.BadStatusLine):
                return (link, default_value)

            finally:
                timeout_obj.cancel()

        return (link, default_value)

    # Pull html for all of the links return a list of tuples in the
    # form [(link, html), ...]
    results = [
        res
        for res
        in pool.imap(pull_link, list(set(uris)))
        ]

    pool.waitall()

    if filter_out_empty_responses:
        results = filter(lambda (link, data): type(data) != None and len(data) > 0, results)

    results = dict(results)

    if treat_results_as_json:
        tmp_dict = {}
        for k, v in results.items():
            try:
                tmp_dict[k] = json.loads(v)
            except ValueError:
                tmp_dict[k] = None

        results = tmp_dict

    return results
