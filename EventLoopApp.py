"""This module is test module."""
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from HTTPParser import HTTPParser
from HTTPResponse import HTTPResponse
from time import ctime
from status import *
import selectors
import signal
import sys
import yaml


sel = selectors.DefaultSelector()

class EventLoopApp:

	def __init__(self, env):
		# Load default setting
		stream = open('env/' + env + '.yaml', 'r')
		config = yaml.load(stream)

		self.HOST = config.get('host')
		self.PORT = config.get('port')
		self.BUFFER_SIZE = config.get('buffer_size')
		self.ADDR = (self.HOST, self.PORT)
		self.SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)

	def accept_client(self, sock, mask):
		CLIENT_SOCKET, ADDR_INFO = sock.accept()
		CLIENT_SOCKET.setblocking(False)
		sel.register(CLIENT_SOCKET, selectors.EVENT_READ, self.read)
		print('[INFO][%s] A client(%s) is connected.' % (ctime(), ADDR_INFO))

	def read(self, CLIENT_SOCKET, mask):
		data = CLIENT_SOCKET.recv(self.BUFFER_SIZE)
		data_size = 0
		data_size += len(data)
		decoded_data = data.decode('utf-8')

		if data_size == 0:
			sel.unregister(CLIENT_SOCKET)
			CLIENT_SOCKET.close()
			print('[INFO][%s] Closed connection from client.')
		elif decoded_data[-2:] != '\r\n':
			print('Bad Request(too long HTTP header)')
			print('Close connection from client') 
			CLIENT_SOCKET.send(HTTPResponse.respond(HTTP_400_BAD_REQUEST))
			sel.unregister(CLIENT_SOCKET)
			CLIENT_SOCKET.close()		
		else:			
			print('[INFO][%s] Received data from client.' % ctime())	
			parser = HTTPParser()
			print('data decoded:' + decoded_data)
			parser.parse(decoded_data)
			connection = parser.get_connect_info()			
			CLIENT_SOCKET.send(HTTPResponse.respond(HTTP_200_OK))
			print('[INFO][%s] Send data to client' % ctime())

			if connection == 'keep-alive':
				pass
			elif connection == 'close':
				# If 'Connection: close', then send the HTTP response back to the client and close the connection.
				sel.unregister(CLIENT_SOCKET)
				CLIENT_SOCKET.close()
				print('[INFO][%s] Closed connection from client.')
		
	def run(self):

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
			events = sel.select()
			for key, mask in events:
				callback = key.data
				print(callback.__name__)
				callback(key.fileobj, mask)


if __name__ == "__main__":
	env = 'development'
	if len(sys.argv) > 1:
		env = sys.argv[1]
	print('Current mode: ' + env)

	app = EventLoopApp(env)
	try:
		app.run()
	except KeyboardInterrupt:
		app.SERVER_SOCKET.close()
		print('You pressed CTRL + C')
		print('Server terminated gracefully')
		



