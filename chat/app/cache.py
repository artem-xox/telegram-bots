from cachetools import MRUCache


cache_messages = MRUCache(maxsize=10)
