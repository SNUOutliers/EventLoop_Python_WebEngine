from cache.fifo_cache import FIFOCache
from cache.lru_cache import LRUCache


DEFAULT_CAPACITY = 50

# Cache policies
LRU = 'lru'
FIFO = 'fifo'


class Cache:
	@staticmethod
	def build(cache_policy=LRU, capacity=DEFAULT_CAPACITY):
		if cache_policy == LRU:
			return LRUCache(capacity)
		elif cache_policy == FIFO:
			return FIFOCache(capacity)

