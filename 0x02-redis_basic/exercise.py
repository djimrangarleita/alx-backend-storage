#!/usr/bin/env python3
"""
Redis basic manipulations
"""
import redis
import uuid
from typing import Union


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
