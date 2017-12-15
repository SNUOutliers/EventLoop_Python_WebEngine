class Event:
	
	def __init__(self, method, request_uri, CLIENT_SOCKET=None):
		self.method = method
		self.request_uri = request_uri
		self.disk_io = False
		self.CLIENT_SOCKET = CLIENT_SOCKET
		self.request_bytes = None
		self.content_type = None
	
	def is_disk_io(self):
		return self.disk_io

	


		
		
