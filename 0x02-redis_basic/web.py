#!/usr/bin/env python3
"""Caching a web page result
"""
import requests
import redis
from functools import wraps


def cache_url_access(fn):
    """Decorator used to cache html page and count url read"""
    rstore = redis.Redis()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """Execute callable and cache result"""
        page_key: str = args[0]
        rstore.incr("count:{}".format(page_key))
        data = rstore.get(page_key)
        if data:
            return data.decode('utf-8')
        data = fn(*args)
        rstore.set(page_key, data, 10)
        return data
    return wrapper


@cache_url_access
def get_page(url: str) -> str:
    """Request a web page and store it's result with an expiration date"""
    r = requests.get(url)
    html_data = r.text
    return html_data
