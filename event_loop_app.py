"""This module is test module."""
import selectors
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from time import ctime

import yaml
from http.status import *

from event import Event
from event_loop import EventLoop
from event_queue import EventQueue
from cache.cache import LRU 
from http.http_parser import HTTPParser
from selector import sel
from utils.event_loop_app_exception import EventLoopAppException

client_info = {}

class EventLoopApp:

	def __init__(self, env, event_queue):
		# Load default setting
		stream = open('env/' + env + '.yaml', 'r')
		config = yaml.load(stream)

		self.HOST = config.get('host')
		self.PORT = config.get('port')
		self.BUFFER_SIZE = config.get('buffer_size')
		self.ADDR = (self.HOST, self.PORT)
		self.SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
		self.event_queue = event_queue		

	def accept_client(self, sock, mask):
		CLIENT_SOCKET, ADDR_INFO = sock.accept()
		CLIENT_SOCKET.setblocking(False)
#		CLIENT_SOCKET.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
		sel.register(CLIENT_SOCKET, selectors.EVENT_READ, self.run)
		#print('[INFO][%s] A client(%s) is connected.' % (ctime(), ADDR_INFO))

	def run(self, CLIENT_SOCKET, mask):
		data = CLIENT_SOCKET.recv(self.BUFFER_SIZE)

		# Receive data from the socket. The return value is a bytes object representing the data received.
		# The maximum amount of data to be received at once is specified by bufsize. 
		data_size = 0
		data_size += len(data)
		decoded_data = data.decode('utf-8')

		if data_size == 0:
			sel.unregister(CLIENT_SOCKET)
			CLIENT_SOCKET.close()
	#		print('Connection from client is disconnected.')		
		else:
			if decoded_data[-2:] != '\r\n':
				print('Bad Request(too long HTTP header)')
				print('Close connection from client') 
				error_event = Event()
				error_event.CLIENT_SOCKET = CLIENT_SOCKET
				raise EventLoopAppException(HTTP_400_BAD_REQUEST, 'Bad Request(too long HTTP header)', error_event)				
			else:
#				print('[INFO][%s] Received data from client.' % ctime())
				parser = HTTPParser()
				event = parser.parse(decoded_data) # Request turned into event.			
				event.CLIENT_SOCKET = CLIENT_SOCKET
				self.event_queue.enqueue(event)			
				
	def start(self):

		self.SERVER_SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		# the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
		# without waiting for its natural timeout to expire.
		self.SERVER_SOCKET.bind(self.ADDR)
		self.SERVER_SOCKET.listen(100)
		self.SERVER_SOCKET.setblocking(False)
		sel.register(self.SERVER_SOCKET, selectors.EVENT_READ, self.accept_client)
		print('Host and Port are successfully binded')
		print('Server Socket is now listening...')

		while True:
			try:
				events = sel.select() # standby here
#				print("Current number of sockets that have things to read:" + str(len(events)))
				for key, mask in events:
					callback = key.data
	#				print(callback.__name__)
					callback(key.fileobj, mask)
			except EventLoopAppException:
				pass


if __name__ == "__main__":
	env = 'development'
	cache_policy = LRU
	if len(sys.argv) > 1:
		env = sys.argv[1]
		if len(sys.argv) == 3:
			cache_policy = sys.argv[2]
	print('Event loop app is starting in ' + env + ' environment with ' + cache_policy + ' cache policy.')

	event_queue = EventQueue()
	app = EventLoopApp(env, event_queue)
	event_loop = EventLoop(event_queue, cache_policy)

	try:
		conn_process = Thread(name='conn_process', target=app.start)
		event_loop_process = Thread(name='event_loop_process', target=event_loop.start)
		conn_process.start()
		event_loop_process.start()
	except KeyboardInterrupt:
		app.SERVER_SOCKET.close()
		print('You pressed CTRL + C')
		print('Server terminated gracefully')
	
