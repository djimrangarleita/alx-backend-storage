#!/usr/bin/env python3
"""
Redis basic manipulations
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a function is called"""
    key: str = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Class that contain methods for redis manip"""

    def __init__(self):
        """Class initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data passed in param in redis"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """Read key from store and return data in specific format"""
        data = self._redis.get(key)
        if fn is None or not data:
            return data
        return fn(data)

    def get_str(self, data: bytes) -> str:
        """Parameterize get for str conversion"""
        return str(data)

    def get_int(self, data) -> int:
        """Parameterize get for int conversion"""
        return int(data)
