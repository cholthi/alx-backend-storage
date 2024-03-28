#!/usr/bin/env python3
""" Provides a redis backed Cache class """
import redis
from typing import Union
import uuid


class Cache:
    """provides caching using redis store"""
    def __init__(self) -> None:
        """Initializes cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a key and stores the data in redis"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
