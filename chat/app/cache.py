from cachetools import MRUCache, LFUCache, LRUCache


class SimpleCache:

    def __init__(self) -> None:
        cache = MRUCache(maxsize=1_000)
    
    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value)
