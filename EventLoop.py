from threading import Thread
from queue import Queue
from HTTPResponse import HTTPResponse
import sys
from status import *
from selector import sel
import os

class EventLoop:

	def __init__(self, event_queue):
		self.event_queue = event_queue
		self.disk_io_queue = Queue()

		for i in range(4):
			t = Thread(target=self.read)
			t.start()
			print("Thread " + str(i) + " started!")

	def start(self):
		while True:
			self.execute()

	def execute(self):
		event = self.event_queue.dequeue()
#		self.event_queue.task_done()
		if event.is_disk_io():
			self.disk_io_queue.put(event)
		else:
			event.CLIENT_SOCKET.send(HTTPResponse.respond(HTTP_200_OK, event))
			sel.unregister(event.CLIENT_SOCKET)
			event.CLIENT_SOCKET.close()
			# Keep-Alive 처리
			print("client connection closed.")			
			# do something

	def read(self):
		while True:
			self.read_aux()

	def read_aux(self):
		event = self.disk_io_queue.get(block=True, timeout=None)
		print("after getting event")
		event = self.process_disk_io(event)
#		self.disk_io_queue.task_done()
		self.event_queue.enqueue(event)
		# Remove and return an item from the queue.
		# if optional args block is true and timeout is None,
		# block if necessary until an item is available.

	def process_disk_io(self, event):
		try:
			with open(os.path.dirname(__file__) + '/resources' + event.request_uri, 'rb') as f:
				event.response_bytes = f.read()
		except: 
			print('File does not exist. Cannot process event')
#			raise Exception('Event Loop terminated')
			sys.exit()

		if event.request_uri.endswith('.jpeg'):
			event.content_type = 'image/jpeg'
		elif event.request_uri.endswith('.html'):
			event.content_type = 'text/html'

		event.disk_io = False
		return event
	
