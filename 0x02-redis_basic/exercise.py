#!/usr/bin/env python3
""" Provides a redis backed Cache class """
import redis
from typing import Union, Optional, Callable
import uuid
import functools


def count_calls(method: Callable) -> Callable:
    """decorator count number of calls of methods in cache class"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        result = method(self, *args, **kwargs)
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

    def get(self, key: str, fn: Callable = None) -> Union[
            str, int, float,  None]:
        """Gets a value for the key in the redis store"""
        data: Union[str, int, float, list, None] = self._redis.get(key)
        if fn is None:
            return data
        return fn(data)

    def get_str(self, data: bytes) -> str:
        """returns data as str"""
        return self.get(data, lambda d: d.decode('utf8'))

    def get_int(self, data: bytes) -> Union[int, None]:
        """returns data as int"""
        return self.get(data, lambda d: int(d))
