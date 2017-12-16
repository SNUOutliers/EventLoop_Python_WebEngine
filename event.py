class Event:
	
	def __init__(self, method, request_uri, disk_io=False):
		self.method = method
		self.request_uri = request_uri
		self.disk_io = disk_io
		self.CLIENT_SOCKET = None
		self.response_bytes = None
		self.set_content_type()

	def set_content_type(self):
		# set content_type by uri
		if self.request_uri.endswith('.jpeg'):
			self.content_type = 'image/jpeg'
		elif self.request_uri.endswith('.html'):
			self.content_type = 'text/html'
		elif self.request_uri.endswith('.mp4'):
			self.content_type = 'video/mp4'

	def is_disk_io(self):
		return self.disk_io
