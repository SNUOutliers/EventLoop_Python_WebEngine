import collections

'''
	More elboration on the code is needed.
	Exception Handling is required.
'''
class FIFOCache:
	def __init__(self, capacity):
		self.capacity = capacity
		self.cache = collections.OrderedDict()

	def get(self, key):
		value = self.cache.get(key)
		if value is None:
			print("FIFO Cache Miss!!!")
			return -1
		
		print("FIFO Cache Hit!!!")
		return value

	def set(self, key, value):
		if self.cache.get(key) is None:
			if len(self.cache) >= self.capacity:
				self.cache.popitem(last=False)
			self.cache[key] = value

