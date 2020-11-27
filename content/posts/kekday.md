---
title: "When is my Cake Day?"
date: "2015-11-20T22:20:00+05:30"
categories: ["tutorial"]
tags: ["python", "reddit", "praw", "prawoauth2"]
slug: "kekday"
description: "Using `praw` and `prawoauth2` to find when is my cake day on Reddit."
---

<a href="https://kekday.herokuapp.com"><img src="{filename}/images/2015/kekday/kekday.png" alt="kek" style="width: 90%;"/></a>

Reddit gives all the user info in a handy JSON at this URL: `https://www.reddit.com/user/<username here>/about.json`

example: [https://www.reddit.com/user/spez/about.json](https://www.reddit.com/user/spez/about.json)

The `created_utc` field in `data` is the date of user's registration aka Cake Day in [unix epoch](https://en.wikipedia.org/wiki/Unix_time) format (in UTC) and we can easily convert that to readable format: 

```python
>>> import time
>>> time.strftime("%D", time.gmtime(1118030400))
'06/06/05'
```

Using [Python Requests](http://python-requests.org), we can turn this into a handy function:

```python
import time
import requests

def get_my_cake_day(username):
    url = "https://www.reddit.com/user/{}/about.json".format(username)
    r = requests.get(url)
    created_at = r.json()['data']['created_utc']
    return time.strftime("%D", time.gmtime(created_at))
```

Though above function will work, but soon it will start throwing HTTP 429 error i.e Too Many Requests. Thing is, Reddit doesn't really like when someone tries to fetch the data like this. The requests are made directly on Reddit servers without using the API. Now if you have want to find cake day of hundreds of users, you cannot use this method.

Solution? Use [Reddit's API](https://www.reddit.com/dev/api). In Python, we will use [praw](https://github.com/praw-dev/praw) and [prawoauth2](https://github.com/avinassh/prawoauth2). praw is a Python wrapper for Reddit's API and prawoauth2 helps dealing with [OAuth2](https://github.com/reddit/reddit/wiki/OAuth2).

Let's start by installing praw:

    pip install praw

Now we can convert the `get_my_cake_day` to praw version and get the user details like this:

```python
import time
import praw

reddit_client = praw.Reddit(user_agent='my amazing cake day bot')

def get_my_cake_day(username):
    redditor = reddit_client.get_redditor(username)
    return time.strftime("%D", time.gmtime(redditor.created_utc))
```

Above code pretty much self explanatory. What if the user doesn't exist or shadowbanned? In such cases, praw throws an exception: `praw.errors.NotFound`. Lets modify `get_my_cake_day` to catch this:

```python
def get_my_cake_day(username):
    try:
        redditor = reddit_client.get_redditor(username)
        return time.strftime("%D", time.gmtime(redditor.created_utc))
    except praw.errors.NotFound:
        return 'User does not exist or shadowbanned'
```

This is better compared to earlier version and we will stop getting rate limit errors often. Also, praw will handle such cases and makes requests again to fetch the data. But what if we want to increase the limit?

The above requests are not authenticated, meaning Reddit does not recognise your app. However, if we register this app in Reddit and let Reddit know, then requests limits will increase. So to authenticate our app over Oauth2, we will use prawoauth2. Lets install it first:

    pip install prawoauth2

Follow the simple steps [here](https://prawoauth2.readthedocs.org/usage_guide.html) to register your app on Reddit. Once done, you will get `app_token` and `app_secret`. Then you need to get `access_token` and `refresh_token`. You could use this handy [`onetime.py`](https://github.com/avinassh/prawoauth2/blob/master/examples/halflife3-bot/onetime.py) script. For detailed instructions check the documentation of [prawoauth2](https://prawoauth2.readthedocs.org). You should never make `app_token`, `app_secret`, `access_token` and `refresh_token` public and never commit them to version control. Keep them always secret.

Here is the complete script using prawoauth2:

```python
import time
import praw

from secret import (app_key, app_secret, access_token, refresh_token,
                    user_agent, scopes)

reddit_client = praw.Reddit(user_agent='my amazing cakeday bot')
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key,
                              app_secret=app_secret,
                              access_token=access_token,
                              refresh_token=refresh_token, scopes=scopes)


def get_my_cake_day(username):
    try:
        redditor = reddit_client.get_redditor(username)
        return time.strftime("%D", time.gmtime(redditor.created_utc))
    except praw.errors.NotFound:
        return 'User does not exists or shadowbanned'
```

Again, pretty much self explanatory. If your tokens are correct and once `PrawOAuth2Mini` is initialized properly, there will be no issues with the app and you will have twice as many requests as compared to unauthenticated version.

Want to see above app in action? Check this - [kekday](https://kekday.herokuapp.com). The [app is open source](https://github.com/avinassh/kekday) and released under MIT License.
