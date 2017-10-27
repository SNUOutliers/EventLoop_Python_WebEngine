"""This module is test module."""
from socket import socket, AF_INET, SOCK_STREAM
from HTTPParser import HTTPParser
import yaml
import sys

class EventLoopApp:
    HOST = 'localhost'
    PORT = 8080
    BUFFER_SIZE = 1024
    ADDR = (HOST, PORT)

    def __init__(self, env):
        stream = open('env/' + env + '.yaml', 'r')
        config = yaml.load(stream)

        self.HOST = config.get('host')
        self.PORT = config.get('port')
        self.BUFFER_SIZE = config.get('buffer_size')
        self.ADDR = (self.HOST, self.PORT)

    def run(self):
        SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
        SERVER_SOCKET.bind(self.ADDR)
        print('bind')

        SERVER_SOCKET.listen(100)
        print('listen')

        while input() != 'quit':
            CLIENT_SOCKET, ADDR_INFO = SERVER_SOCKET.accept()
            print('Client Socket')
            print(CLIENT_SOCKET)
            print('Address Information')
            print(ADDR_INFO)
            print('accept')
            print('Received data')
            print(HTTPParser.parse(CLIENT_SOCKET.recv(self.BUFFER_SIZE).decode('utf-8')))
            CLIENT_SOCKET.send('Thanks for connecting\n'.encode('utf-8'))
            CLIENT_SOCKET.close()
            print('close connection for client')

        SERVER_SOCKET.close()
        print('EventLoopApp quitted gracefully.')

if __name__ == "__main__":
    env = 'development'
    if len(sys.argv) > 1:
        env = sys.argv[1]

    app = EventLoopApp(env)
    app.run()



