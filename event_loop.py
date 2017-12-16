from threading import Thread
from queue import Queue
from http_response import HTTPResponse
import sys
from status import *
from selector import sel
import os
from utils.event_loop_app_exception import EventLoopAppException
from cache import LRUCache

CACHE_CAPACITY = 50
NUM_OF_THREADS = 4

class EventLoop:

	def __init__(self, event_queue):
		self.event_queue = event_queue
		self.disk_io_queue = Queue()
		self.lru_cache = LRUCache(CACHE_CAPACITY)

		for i in range(NUM_OF_THREADS):
			t = Thread(target=self.read)
			t.start()
			print("Thread " + str(i) + " started!")

	def start(self):
		while True:
			self.execute()

	def execute(self):
		event = self.event_queue.dequeue()
		if event.is_disk_io():
			# Check whether the requested data is cached.
			cached_response_bytes = self.lru_cache.get(event.request_uri)

			if cached_response_bytes != -1:
				event.response_bytes = cached_response_bytes
				event.disk_io = False
				self.event_queue.enqueue(event)
			else:
				self.disk_io_queue.put(event)
		else:
			event.CLIENT_SOCKET.send(HTTPResponse.respond(HTTP_200_OK, event))
			EventLoop.close_or_keep_alive(event)

	@staticmethod
	def close_or_keep_alive(event):		
		if event.connection == 'keep-alive':
			pass
		else:
			sel.unregister(event.CLIENT_SOCKET)
			event.CLIENT_SOCKET.close()
			print("Connection from client is closed.")

	def send_event(self, event):
		print("Event sending started!")
		bytes_to_send = HTTPResponse.respond(HTTP_200_OK, event)
		event.CLIENT_SOCKET.setblocking(True)
		total_sent = 0
		while total_sent < len(bytes_to_send):
			sent = event.CLIENT_SOCKET.send(bytes_to_send[total_sent:total_sent + 1024*8*8])
			total_sent = total_sent + sent
			print("%d / %d sent!"%(total_sent, len(bytes_to_send)))
		print("Event Sent!")

	def read(self):
		while True:
			self.read_aux()

	def read_aux(self):
		event = self.disk_io_queue.get(block=True, timeout=None)
		print("after getting event")
		event = self.process_disk_io(event)
#		self.disk_io_queue.task_done()
		self.event_queue.enqueue(event)

	def process_disk_io(self, event):
		print("Read file from disk.")
		try:
			with open(os.path.dirname(__file__) + '/resources' + event.request_uri, 'rb') as f:
				event.response_bytes = f.read()
				# Newly read file is inserted into cache.
				self.lru_cache.set(event.request_uri, event.response_bytes)
		except: 
			raise EventLoopAppException(HTTP_404_NOT_FOUND, 'File does not exist. Cannot process event', event)

		event.disk_io = False
		print("Done reading file from disk.")
		return event
