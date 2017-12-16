import collections

'''
	More elboration on the code is needed.
	Exception Handling is required.
'''
class LRUCache:
	def __init__(self, capacity):
		self.capacity = capacity
		self.cache = collections.OrderedDict()

	def get(self, key):
		try:			
			value = self.cache.pop(key)
			self.cache[key] = value
			print("Cache Hit!!!")
			return value
		except KeyError:
			print("Cache Miss!!")
			return -1

	def set(self, key, value):
		try:
			self.cache.pop(key)
		except KeyError:
			if len(self.cache) >= self.capacity:
				self.cache.popitem(last=False)
		self.cache[key] = value
