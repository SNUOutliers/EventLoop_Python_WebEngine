import collections
import sys

'''
	More elboration on the code is needed.
	Exception Handling is required.
'''
class LRUCache:
	def __init__(self, capacity, size):
		self.capacity = capacity
		self.cache = collections.OrderedDict()
		self.size = size
		self.current_size = 0

	def get(self, key):
		try:			
			value = self.cache.pop(key)
			self.cache[key] = value
			#print("LRU Cache Hit!")
			return value
		except KeyError:
			#print("LRU Cache Miss!")
			return -1

	def set(self, key, value):
		if sys.getsizeof(value) > 10 * 1024 * 1024:
			return
		try:
			self.cache.pop(key)
		except KeyError:
			if len(self.cache) >= self.capacity:
				item = self.cache.popitem(last=False)
				self.current_size = self.current_size - sys.getsizeof(item)
			while self.size < self.current_size + sys.getsizeof(value):
				item = self.cache.popitem(last=False)
				self.current_size = self.current_size - sys.getsizeof(item)		 
		self.cache[key] = value
		self.current_size = self.current_size + sys.getsizeof(value)

