class EventQueue:
	def __init__(self):
		self._queue = self.Queue()		

	def enqueue(self, event):
		self._queue.enqueue(event)

	def dequeue(self):
		if not self._queue.isEmpty():
			return self._queue.dequeue()
		else:
			return None
		
	class Queue:
	# This queue is simply implemented without using lock.
	#	If an error occurs, should implement lock.
	#	Can the length of a Queue be a meaningful parameter?
		def __init__(self):
			self._list = []
		def enqueue(self, event):
			self._list.append(event)
	
		def isEmpty(self):
			return len(self._list) == 0
		
		def dequeue(self):
			return self._list.pop(0)
