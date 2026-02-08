from functools import lru_cache
import asyncio
from typing import Any

# Simple in-memory cache using lru_cache
# Note: This is per-process. For production with multiple workers, allow redis.
# But for this task, in-memory is sufficient and fast.

@lru_cache(maxsize=100)
def get_cached_response(query: str):
    # This is a placeholder. 
    # Realistically, we can't cache async calls or complex objects easily with standard lru_cache 
    # if we want to wrap the whole pipeline.
    # So we'll implement a simple dictionary-based async-compatible cache.
    pass

class SimpleCache:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key: str):
        if key in self.cache:
            # Move to end (most recently used)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None

    def set(self, key: str, value: Any):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Evict least recently used (first in list)
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)

# Global cache instance
query_cache = SimpleCache(capacity=200)
