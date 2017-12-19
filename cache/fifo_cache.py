import collections
import sys


'''
	More elboration on the code is needed.
	Exception Handling is required.
'''
class FIFOCache:
	def __init__(self, capacity, size):
		self.capacity = capacity
		self.cache = collections.OrderedDict()
		self.size = size
		self.current_size = 0

	def get(self, key):
		value = self.cache.get(key)
		if value is None:
			print("FIFO Cache Miss!!!")
			return -1
		
		print("FIFO Cache Hit!!!")
		return value

	def set(self, key, value):
		if sys.getsizeof(value) > 10 * 1024 * 1024:
			return 
		if self.cache.get(key) is None:
			if len(self.cache) >= self.capacity:
				item = self.cache.popitem(last=False)
				self.current_size = self.current_size - sys.getsizeof(item)
			while self.size < self.current_size + sys.getsizeof(value):
				item = self.cache.popitem(last=False)
				self.current_size = self.current_size - sys.getsizeof(item)	
			self.cache[key] = value
			self.current_size = self.current_size + sys.getsizeof(value)

