"""This module is test module."""
from socket import socket, AF_INET, SOCK_STREAM

HOST = 'localhost'
PORT = 8080
BUFSIZE = 1024
ADDR = (HOST, PORT)

SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(ADDR)
print('bind')

SERVER_SOCKET.listen(100)
print('listen')

while 1:
    CLIENT_SOCKET, ADDR_INFO = SERVER_SOCKET.accept()
    print('Client Socket')
    print(CLIENT_SOCKET)
    print('Address Information')
    print(ADDR_INFO)
    print('accept')

    CLIENT_SOCKET.send('Thanks for connecting\n')
    CLIENT_SOCKET.close()
    print('close connection for client')

SERVER_SOCKET.close()
print('close')
