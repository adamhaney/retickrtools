"""
This module converts facebook posts from the newstream into a common story format
"""

import iso8601
import requests


def parse_status(story):
    """

    Parses one of Facebook's 'status' objects from the news feed.
    This object's fields are described at:
    http://developers.facebook.com/docs/reference/api/status/


    >>> status_obj = {
    ... "from": {
    ... "category": "Website",
    ... "name": "Google",
    ... "id": "104958162837"
    ... },
    ... "actions": [
    ... {
    ... "link": "http://www.facebook.com/104958162837/posts/10150603726957838",
    ... "name": "Comment"
    ... },
    ... {
    ... "link": "http://www.facebook.com/104958162837/posts/10150603726957838",
    ... "name": "Like"
    ... }
    ... ],
    ... "updated_time": "2012-02-11T01:10:00+0000",
    ... "likes": {
    ... "count": 652,
    ... "data": [
    ... {
    ... "name": "Michal Henryk Balk\u0131z",
    ... "id": "1526114242"
    ... }
    ... ]
    ... },
    ... "created_time": "2012-02-11T01:10:00+0000",
    ... "message": "Have a great weekend!",
    ... "type": "status",
    ... "id": "104958162837_10150603726957838",
    ... "comments": {
    ... "count": 64
    ... }
    ... }

    >>> status = Facebook.parse_fb_status_message(status_obj)

    >>> status["author"]
    'Google'

    >>> status["title"]
    'Have a great weekend!'

    >>> status["content"]
    'Have a great weekend!'

    >>> status["link"]
    'http://www.facebook.com/104958162837/posts/10150603726957838'

    """

    story_obj = {
        "author": story.get("from", {}).get("name", ""),
        "title": story.get("message", "")[:420],
        "content": story.get("message", ""),
        "link": ""
        }

    for action in story.get("actions", []):
        if action["name"] == "Comment":
            story_obj["link"] = action["link"].encode("utf-8")

    return story_obj


def parse_link(story):
    """
    Parses one of Facebook's 'link' objects from the news feed.
    This object's fields are described at:
    http://developers.facebook.com/docs/reference/api/link/

    >>> link_obj = {
    ... "picture": "http://platform.ak.fbcdn.net/www/app_full_proxy.php?app=187663324592154&v=1&size=z&cksum=865e5b51c6b2bb9236cb25fc8c42b569&src=http%3A%2F%2Fd1ex7czhcknhxx.cloudfront.net%2Fxpgrlv142i8rwwg4wdfj6um66a3q60bk_265x149.jpg",
    ... "from": {
    ... "name": "Jennifer Van Grove",
    ... "id": "714437681"
    ... },
    ... "name": "The Facebook before it was famous",
    ... "application": {
    ... "id": "187663324592154",
    ... "namespace": "chilllive",
    ... "name": "Chill",
    ... "canvas_name": "chilllive"
    ... },
    ... "comments": {
    ... "count": 1,
    ... "data": [
    ... {
    ... "created_time": "2012-02-11T01:05:46+0000",
    ... "message": "Saw this a long time ago. Funny, huh?",
    ... "from": {
    ... "name": "Hardy Case",
    ... "id": "1133868424"
    ... },
    ... "id": "714437681_254700151271098_1864957"
    ... }
    ... ]
    ... },
    ... "actions": [
    ... {
    ... "link": "http://www.facebook.com/714437681/posts/254700151271098",
    ... "name": "Comment"
    ... },
    ... {
    ... "link": "http://www.facebook.com/714437681/posts/254700151271098",
    ... "name": "Like"
    ... },
    ... {
    ... "link": "http://chill.com/ChasGessner/post/e0096b7253bb11e1b988123140ff5ed9/the-facebook-before-it-was-famous?utm_campaign=user_post_sharing&utm_content=e0096b7253bb11e1b988123140ff5ed9&utm_medium=facebook&utm_source=users&utm_term=anonymous",
    ... "name": "Watch this video"
    ... }
    ... ],
    ... "updated_time": "2012-02-11T01:05:46+0000",
    ... "caption": "A video shared on Chill",
    ... "link": "http://chill.com/ChasGessner/post/e0096b7253bb11e1b988123140ff5ed9/the-facebook-before-it-was-famous?utm_campaign=user_post_sharing&utm_content=e0096b7253bb11e1b988123140ff5ed9&utm_medium=facebook&utm_source=users&utm_term=anonymous",
    ... "likes": {
    ... "count": 13,
    ... "data": [
    ... {
    ... "name": "Sonny Uppal",
    ... "id": "100002367467204"
    ... }
    ... ]
    ... },
    ... "created_time": "2012-02-11T00:58:24+0000",
    ... "message": "a blast from the past",
    ... "icon": "http://photos-f.ak.fbcdn.net/photos-ak-snc1/v43/138/187663324592154/app_2_187663324592154_4473.gif",
    ... "type": "link",
    ... "id": "714437681_254700151271098",
    ... "description": "More at http://www.systemseminartv.com"
    ... }

    >>> link = Facebook.parse_fb_link(link_obj)

    >>> link["author"]
    'Jennifer Van Grove'

    >>> link["title"]
    'a blast from the past'

    >>> link["content"]
    'a blast from the past More at http://www.systemseminartv.com'

    >>> link["link"]
    'http://www.facebook.com/714437681/posts/254700151271098'

    """

    story_obj = {
        "author": story.get("from", {}).get("name", ""),
        "title": story.get("message", "")[:420],
        "content": "{0} {1}".format(
            story.get("message", ""),
            story.get("description", "")
            ),
        "link": ""
        }

    for action in story.get("actions", []):
        if action["name"] == "Comment":
            story_obj["link"] = action["link"].encode("utf-8")

    return story_obj


def parse_photo(story):
    """
    Parses one of Facebook's 'photo' object from the news feed.
    This object's fields are described at:
    http://developers.facebook.com/docs/reference/api/photo/

    >>> photo_obj = {
    ... "picture": "http://photos-f.ak.fbcdn.net/hphotos-ak-ash4/404203_10150653737331558_14408401557_11421762_238204971_s.jpg",
    ... "likes": {
    ... "count": 105,
    ... "data": [
    ... {
    ... "name": "Tiffany Ring",
    ... "id": "787364103"
    ... }
    ... ]
    ... },
    ... "from": {
    ... "category": "Product/service",
    ... "name": "Amazon Kindle",
    ... "id": "14408401557"
    ... },
    ... "comments": {
    ... "count": 21,
    ... "data": [
    ... {
    ... "created_time": "2012-02-11T01:07:32+0000",
    ... "message": "how about a Free one-day kindle sale?",
    ... "from": {
    ... "name": "Briana Carrillo",
    ... "id": "100001501042219"
    ... },
    ... "id": "14408401557_10150653737361558_7087992"
    ... },
    ... {
    ... "created_time": "2012-02-11T01:08:37+0000",
    ... "message": "Just got my Fire a few days ago. I would love this!!!",
    ... "from": {
    ... "name": "Michelle Lopez",
    ... "id": "1783494795"
    ... },
    ... "id": "14408401557_10150653737361558_7087998"
    ... }
    ... ]
    ... },
    ... "actions": [
    ... {
    ... "link": "http://www.facebook.com/14408401557/posts/10150653737361558",
    ... "name": "Comment"
    ... },
    ... {
    ... "link": "http://www.facebook.com/14408401557/posts/10150653737361558",
    ... "name": "Like"
    ... }
    ... ],
    ... "updated_time": "2012-02-11T01:08:37+0000",
    ... "link": "http://www.facebook.com/photo.php?fbid=10150653737331558&set=a.196041166557.167046.14408401557&type=1",
    ... "object_id": "10150653737331558",
    ... "created_time": "2012-02-11T00:52:42+0000",
    ... "message": "How do you ask a Kindle lover to be your Valentine? Here's an idea that comes with free one-day shipping. http://amzn.to/z3IeW9",
    ... "type": "photo",
    ... "id": "14408401557_10150653737361558",
    ... "icon": "http://static.ak.fbcdn.net/rsrc.php/v1/yz/r/StEh3RhPvjk.gif"
    ... }

    >>> photo = Facebook.parse_fb_photo(photo_obj)

    >>> photo["author"]
    'Amazon Kindle'

    >>> photo["title"]
    'Amazon Kindle added a new photo'

    >>> photo["content"]
    "<img src='http://photos-f.ak.fbcdn.net/hphotos-ak-ash4/404203_10150653737331558_14408401557_11421762_238204971_s.jpg' />"

    >>> photo["link"]
    'http://www.facebook.com/photo.php?fbid=10150653737331558&set=a.196041166557.167046.14408401557&type=1'

    """

    author = story.get("from", {}).get("name", "")
    story_obj = {
        "author": author,
        "title": story.get(
            "story", "{0} added a new photo".format(author)),
        "content": "<img src='{0}' />".format(story.get("picture", "")),
        "link": story.get("link", "")
        }

    return story_obj


def parse_video(story):
    """
    Parses one of Facebook's 'video' object from the news feed.
    This object's fields are described at:
    http://developers.facebook.com/docs/reference/api/video/

    >>> video_obj = {
    ... "picture": "http://vthumb.ak.fbcdn.net/hvthumb-ak-ash4/410484_10150565862884947_10150565851104947_52486_1313_t.jpg",
    ... "from": {
    ... "name": "Timothy Anderson",
    ... "id": "635214946"
    ... },
    ... "name": "Where's Eric?!",
    ... "object_id": "10150565851104947",
    ... "message_tags": {
    ... "9": [
    ... {
    ... "length": 9,
    ... "offset": 9,
    ... "type": "user",
    ... "id": "100001079624283",
    ... "name": "Eric Fung"
    ... }
    ... ]
    ... },
    ... "comments": {
    ... "count": 0
    ... },
    ... "actions": [
    ... {
    ... "link": "http://www.facebook.com/635214946/posts/10150565851104947",
    ... "name": "Comment"
    ... },
    ... {
    ... "link": "http://www.facebook.com/635214946/posts/10150565851104947",
    ... "name": "Like"
    ... }
    ... ],
    ... "properties": [
    ... {
    ... "text": "1:35",
    ... "name": "Length"
    ... }
    ... ],
    ... "to": {
    ... "data": [
    ... {
    ... "name": "Eric Fung",
    ... "id": "100001079624283"
    ... }
    ... ]
    ... },
    ... "application": {
    ... "id": "2392950137",
    ... "namespace": "video",
    ... "name": "Video",
    ... "canvas_name": "video"
    ... }
    ... }

    >>> video = Facebook.parse_fb_video(video_obj)

    >>> video["author"]
    'Timothy Anderson'

    >>> video["title"]
    "Where's Eric?!"

    >>> video["content"]
    "Where's Eric?!"

    >>> video["link"]
    'http://www.facebook.com/635214946/posts/10150565851104947'

    """

    author = story.get("from", {}).get("name", "")
    story_obj = {
        "author": author,
        "title": story.get("name", "{0} shared a video {1}".format(
                author,
                story.get("name", ""))),
        "content": story.get("name", "{0} shared a video {1}".format(
                author,
                story.get("name", ""))),
        "link": story.get("link", "")
        }

    for action in story.get("actions", []):
        if action["name"] == "Comment":
            story_obj["link"] = action["link"].encode("utf-8")

    return story_obj


def parse_question(story):
    author = story.get("from", {}).get("name", "")
    story_obj = {
        "author": author,
        "title": story.get("story", "{0} asked a question"),
        "content": story.get("story", "{0} asked a question"),
        "link": story.get("link", "")
        }

    return story_obj


def parse_checkin(story):
    author = story.get("from", {}).get("name", "")
    story_obj = {
        "author": author,
        "title": story.get("caption", "{0} checked in at {1}".format(
                author,
                story.get("name", "")
                )),
        "content": story.get("description", ""),
        "link": ""
        }

    for action in story.get("actions", []):
        if action["name"] == "Comment":
            story_obj["link"] = action["link"].encode("utf-8")

    return story_obj

_parse_functions = {
    "status": parse_status,
    "link": parse_link,
    "photo": parse_link,
    "video": parse_video,
    "question": parse_question,
    "checkin": parse_checkin
    }

api_endpoint = "https://graph.facebook.com"

def get_stories(oauth_token):
    raw_stories = requests.get(
        "{0}/me/home?access_token={1}".format(
            api_endpoint,
            oauth_token
            )
        ).json["data"]

    stories = []

    for story in raw_stories:
        if story["type"] in _parse_functions:
            clean_story = _parse_functions[story["type"]](story)

            clean_story["update_time"] = iso8601.parse_date(
                story.get("created_time", "")
                )

            if "from" in story and id in story["from"]:
                clean_story["icon_url"] = "{0}/{1}/picture".format

            stories.append(clean_story)

    return stories

