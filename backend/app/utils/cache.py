"""
Jinja SSS Platform - Simple Cache Manager
"""

import time
from functools import wraps


class SimpleCache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            del self._cache[key]
        return None

    def set(self, key, value, ttl=60):
        self._cache[key] = (value, time.time() + ttl)

    def delete(self, key):
        self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()


cache = SimpleCache()


def cached(ttl=60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            result = cache.get(key)
            if result is not None:
                return result
            result = await func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator
