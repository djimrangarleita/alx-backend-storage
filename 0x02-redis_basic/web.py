#!/usr/bin/env python3
"""Caching a web page result
"""
import redis
import requests
from functools import wraps
from typing import Callable


def cache_url_access(fn: Callable) -> Callable:
    """Decorator used to cache html page and count url read"""
    @wraps(fn)
    def wrapper(url: str) -> str:
        """Execute callable and cache result"""
        rstore = redis.Redis()
        rstore.incr("count:{}".format(url))
        data = rstore.get(url)
        if data:
            return data.decode('utf-8')
        html_data = fn(url)
        rstore.set(url, html_data, ex=10)
        return html_data
    return wrapper


@cache_url_access
def get_page(url: str) -> str:
    """Request a web page and store it's result with an expiration date"""
    r = requests.get(url)
    return r.text
