#!/usr/bin/env python3
"""Fetches a remote url and tracks url hits uisng a redis store"""
import requests
import redis
from functools import wraps
from typing import Callable

store = redis.Redis()
"""Redis instance"""


def count_hits(fn: Callable) -> Callable:
    """Tracks how many times a url was hit in fn"""
    '''Caches the output of fetched data
    '''
    @wraps(fn)
    def invoker(url) -> str:
        '''The wrapper function for caching the output
        '''
        store.incr(f'count:{url}')
        result = store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = fn(url)
        store.set(f'count:{url}', 0)
        store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@count_hits
def get_page(url: str) -> str:
    """Fetches a remote url content"""
    return requests.get(url).text
