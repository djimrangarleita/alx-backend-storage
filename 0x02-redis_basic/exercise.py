#!/usr/bin/env python3
"""
Redis basic manipulations
"""
import redis
import uuid
from typing import Callable, Union


class Cache:
    """Class that contain methods for redis manip"""

    def __init__(self):
        """Class initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data passed in param in redis"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """Read key from store and return data in specific format"""
        data = self._redis.get(key)
        if not data:
            return
        if not fn and isinstance(data, str):
            fn = self.get_int
        elif not fn:
            fn = self.get_str
        return fn(data)

    def get_str(self, data: bytes) -> str:
        """Parameterize get for str conversion"""
        return str(data)

    def get_int(self, data) -> int:
        """Parameterize get for int conversion"""
        return int(data)
