#!/usr/bin/env python3
""" Provides a redis backed Cache class """
import redis
from typing import Union, Optional, Callable
import uuid
import functools


def count_calls(fn):
    """decorator count number of calls of methods in cache class"""
    @functools.wraps(fn)
    def wrapper(self, data):
        self._redis.incr(fn.__qualname__)
        result = fn(self, data)
        return result
    return wrapper

class Cache:
    """provides caching using redis store"""
    def __init__(self) -> None:
        """Initializes cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a key and stores the data in redis"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable[[], None]]=None) -> Union[
            str, int, float, list, None]:
        """Gets a value for the key in the redis store"""
        data: Union[str, int, float, list, None] = self._redis.get(key)
        if data is None or fn is None:
            return data
        try:
            return fn(data)
        except ValueError:
            return None

    def get_str(self, data: bytes) -> str:
        """returns data as str"""
        return data.decode('utf8')

    def get_int(self, data: bytes) -> Union[int, None]:
        """returns data as int"""
        try:
            return int(data)
        except ValueError:
            return None
