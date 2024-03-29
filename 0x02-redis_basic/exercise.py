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


def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs and outputs for
    a Cache class methods
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush('{}:inputs'.format(
                method.__qualname__), str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush('{}:outputs'.format(
                method.__qualname__), output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """Display the history of calls of a particular function fn"""
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return

    input_key = '{}:inputs'.format(fn.__qualname__)
    output_key = '{}:outputs'.format(fn.__qualname__)
    fn_name = fn.__qualname__

    if redis_store.exists(fn_name) != 0:
        call_count = int(redis_store.get(fn_name))
        print('{} was called {} times:'.format(fn_name, call_count))
    inputs_history = redis_store.lrange(input_key, 0, -1)
    outputs_history = redis_store.lrange(output_key, 0, -1)
    for i, o in zip(inputs_history, outputs_history):
        print('{}(*{}) -> {}'.format(fn_name, i.decode('utf8'), o))


class Cache:
    """provides caching using redis store"""
    def __init__(self) -> None:
        """Initializes cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
