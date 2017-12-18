"""Custom exception handler."""
from http.http_response import HTTPResponse
from selector import sel


class EventLoopAppException(Exception):
	def __init__(self, status_code, message, event):
		Exception.__init__(self)
		self.message = message

		event.response_bytes = message.encode('utf-8')
		
		event.CLIENT_SOCKET.send(HTTPResponse.respond(status_code, event))
		sel.unregister(event.CLIENT_SOCKET)
		event.CLIENT_SOCKET.close()

