class Event:
	
	def __init__(self, method, request_uri, disk_io=False):
		self.method = method
		self.request_uri = request_uri
		self.disk_io = disk_io
		self.CLIENT_SOCKET = None
		self.response_bytes = None
		self.content_type = None
	
	def is_disk_io(self):
		return self.disk_io

