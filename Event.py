class Event:
	
	def __init__(self, method, request_uri):
		self.method = method
		self.request_uri = request_uri
		self.disk_io = False
		
	def is_disk_IO(self):
		return self.disk_io
		
		
