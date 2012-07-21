#!/usr/bin/env python
"""
Retickr Data Model Constants File

We use various magic numbers, hardcoded URLs, etc throughout
retickr.  Here we attempt to localize them all.
"""
#redirect_url = "http://cdn.retickr.com/story_redirect"
#icon_cdn_url = "http://cdn.retickr.com/icons"
redirect_url = "http://10.100.90.2:1985/story_redirect"
icon_cdn_url = "http://10.100.90.2:1985/icons"

cannonical_rtkr_datetime_format = "%Y-%m-%dT%H:%M:%SZ"

# Definition of the stories that should be shown when a playlist is empty
empty_playlist_stories = [
    {
        "author": "retickr",
        "feed_url": "http://about.retickr.com/feed",
        "title": "This playlist doesn't have any stories, yet",
        "content": ("You are attempting to stream a playlist"
        + "without any stories. Click the link to read more"),
        "link": "http://about.retickr.com/why-dont-i-see-any-stories/",
        "type": "RSS",
        "icon_url": "{0}/c0086f90b2e54dea5482a3212dd590e0".format(
            icon_cdn_url),
        "feed_meta":
            {
            "title": "retickr"
            }
        },
    {
        "author": "retickr",
        "feed_url": "http://about.retickr.com/feed",
        "title": "While we have you here... survey?",
        "content": ("You've attempted to stream a playlist that"
        + " doesn't have any stories. If you have some time please"
        + " fill out a quick survey"),
        "link": "http://about.retickr.com/survey",
        "type": "RSS",
        "icon_url": "{0}/c0086f90b2e54dea5482a3212dd590e0".format(
            icon_cdn_url),
        "feed_meta":
            {
            "title": "retickr"
            }
        },
    {
        "author": "retickr",
        "feed_url": "http://about.retickr.com/feed",
        "title": "Tips and Tricks",
        "content": ("You are attempting to stream a playlist"
        + " without any stories. Read our tips and tricks section for"
        + " more information"),
        "link": "http://about.retickr.com/retickr-2-0-tips-and-tricks/",
        "type": "RSS",
        "icon_url": "{0}/c0086f90b2e54dea5482a3212dd590e0".format(
            icon_cdn_url),
        "feed_meta":
            {
            "title": "retickr"
            }
        }
    ]

connection_timeout = 15
