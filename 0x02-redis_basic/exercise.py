#!/usr/bin/env python3
"""
Redis basic manipulations
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def replay(method: Callable):
    """Display history of function call"""
    key: str = method.__qualname__
    instance = method.__self__
    inputs = instance._redis.lrange("{}:inputs".format(key), 0, -1)
    outputs = instance._redis.lrange("{}:outputs".format(key), 0, -1)
    print("{} was called {} times:".format(key, len(inputs)))
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key,
                                     i.decode('utf-8'),
                                     o.decode('utf-8')))


def call_history(method: Callable) -> Callable:
    """Decorate some methods and keeps their call history"""
    key: str = method.__qualname__

    @wraps(method)
    def wrapper(self, *args):
        """Wrapper fn to execute before method"""
        self._redis.rpush("{}:inputs".format(key), str(args))
        out = method(self, *args)
        self._redis.rpush("{}:outputs".format(key), out)
        return out
    return wrapper


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

    @call_history
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
