from cache.fifo_cache import FIFOCache
from cache.lru_cache import LRUCache


DEFAULT_CAPACITY = 50
DEFAULT_SIZE = 200 * 1024 * 1024

# Cache policies
LRU = 'lru'
FIFO = 'fifo'


class Cache:
	@staticmethod
	def build(cache_policy=LRU, capacity=DEFAULT_CAPACITY, size=DEFAULT_SIZE):
		if cache_policy == LRU:
			return LRUCache(capacity, size)
		elif cache_policy == FIFO:
			return FIFOCache(capacity, size)

