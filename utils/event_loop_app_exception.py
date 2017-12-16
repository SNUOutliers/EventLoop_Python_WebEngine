"""Custom exception handler."""
from selector import sel
from http_response import HTTPResponse


class EventLoopAppException(Exception):
	def __init__(self, status_code, message, event):
		Exception.__init__(self)
		self.message = message

		event.response_bytes = message.encode('utf-8')
		
		event.CLIENT_SOCKET.send(HTTPResponse.respond(status_code, event))
		sel.unregister(event.CLIENT_SOCKET)
		event.CLIENT_SOCKET.close()

