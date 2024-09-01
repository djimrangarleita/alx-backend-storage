#!/usr/bin/env python3
"""Caching a web page result
"""
import requests
import redis
from functools import wraps
from typing import Callable


def cache_url_access(fn: Callable) -> Callable:
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
        rstore.set(page_key, data, ex=10)
        return data
    return wrapper


def get_page(url: str) -> str:
    """Request a web page and store it's result with an expiration date"""
    rstore = redis.Redis()
    rstore.incr("count:{}".format(url))
    data = rstore.get(url)
    if data:
        return data.decode('utf-8')
    r = requests.get(url)
    html_data = r.text
    rstore.set(url, html_data, ex=10)
    return html_data
