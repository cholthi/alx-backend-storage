#!/usr/bin/env python3
""" Provides a redis backed Cache class """
import redis
from typing import Union, Optional, Callable
import uuid


class Cache:
    """provides caching using redis store"""
    def __init__(self) -> None:
        """Initializes cache class"""
        self._redis = redis.Redis(password='foobared')
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a key and stores the data in redis"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable[[], None]]) -> Union[
            str, int, float, list, None]:
        """Gets a value for the key in the redis store"""
        data: Union[str, int, float, list, None] = self._redis.get(key)
        if data is None or fn is None:
            return data
        return fn(data)

    def get_str(self, data: bytes) -> str:
        """returns data as str"""
        return data.decode('utf8')

    def get_int(self, data: bytes) -> Union[int, None]:
        """returns data as int"""
        try:
            return int(data)
        except ValueError:
            return None
