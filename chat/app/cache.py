from cachetools import MRUCache
from typing import Optional

from messages import Chat


class BaseCache:

    def get(self, key) -> Optional[Chat]:
        raise NotImplemented()

    def set(self, key, value) -> None:
        raise NotImplemented()


class SimpleCache(BaseCache):

    def __init__(self):
        self.cache = MRUCache(maxsize=1_000)
    
    def get(self, key) -> Optional[Chat]:
        return self.cache.get(key)

    def set(self, key, value) -> None:
        self.cache[key] = value

    def delete(self, key) -> bool:
        if key in self.cache:
            self.cache.pop(key)
            return True
        return False