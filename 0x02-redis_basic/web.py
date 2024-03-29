#!/usr/bin/env python3
"""Fetches a remote url and tracks url hits uisng a redis store"""
import requests
import redis
from functools import wraps
from typing import Callable


def count_hits(fn: Callable) -> Callable:
    """Tracks how many times a url was hit in fn"""
    store = redis.Redis(password='foobared')

    @wraps(fn)
    def wrapper(url):
        key = 'count:{}'.format(url)
        store.incr(key)
        result = store.get('cache:{}'.format(url))
        if result:
            return result.decode('utf8')
        result = fn(url)
        store.set('count:{}'.format(url), 0)
        store.set('cache:{}'.format(url), result, ex=10)
        return result
    return wrapper


@count_hits
def get_page(url: str) -> str:
    """Fetches a remote url content"""
    return requests.get(url).text
