"""This module is test module."""
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from HTTPParser import HTTPParser
from HTTPResponse import HTTPResponse
import yaml
import sys
import signal
import time

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

	def run(self):

		self.SERVER_SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		# the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
		# without waiting for its natural timeout to expire.
		self.SERVER_SOCKET.bind(self.ADDR)
		self.SERVER_SOCKET.listen(100)
		print('Host and Port are successfully binded')
		print('Server Socket is now listening...')

		while True:
			CLIENT_SOCKET, ADDR_INFO = self.SERVER_SOCKET.accept()
			print('Client Socket is connected')
			print('Address Information: ' + str(ADDR_INFO))
			CLIENT_SOCKET.send(HTTPResponse().respond().encode('utf-8')) # test

			# 여기서 pause 발생
			# request를 두 번 날려야 다음으로 이어짐.
			# 여기서 recv를 바로 하지 않는 이유?

			data = CLIENT_SOCKET.recv(self.BUFFER_SIZE) # 한 번 받고, 
			data_size = 0
			data_size += len(data)		

			if len(CLIENT_SOCKET.recv(self.BUFFER_SIZE)) > 0: # 잔여 데이터가 남았다면
				print('Bad Request(too long HTTP header)')
				print('Close connection from client') 
				CLIENT_SOCKET.close() # 연결되어 있는 클라이언트와의 연결을 끊고, 다시 처음으로 
				continue

			print("The size of data: " + str(data_size))
			parser = HTTPParser()
			parser.parse(data.decode('utf-8'))
			connection = parser.get_connect_info()
			
#			print(HTTPParser().parse(data.decode('utf-8')))
			CLIENT_SOCKET.send(HTTPResponse().respond().encode('utf-8'))
			CLIENT_SOCKET.close()
			print('close connection for client')
		
		self.SERVER_SOCKET.close()
		print('EventLoopApp terminated gracefully.')


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
		

#	try:
#	except (Exception, KeyboardInterrupt) as e:

#	print(e)
#	app.SERVER_SOCKET.close()		
#	print('EventLoopApp terminated gracefully.')

# list index out of range
