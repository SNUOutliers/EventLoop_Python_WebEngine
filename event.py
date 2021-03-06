class Event:
	
	def __init__(self, method='GET', request_uri='/', disk_io=False, connection='keep-alive'):
		self.method = method
		self.request_uri = request_uri
		self.disk_io = disk_io
		self.CLIENT_SOCKET = None
		self.response_bytes = b'Welcome to group G\'s Event Loop Web Engine' # changed from None to b''
		self.set_content_type()
		self.connection = connection

	def set_content_type(self):
		# set content_type by uri
		if self.request_uri.endswith('.html'):
			self.content_type = 'text/html'
		else:
			self.content_type = '*/*'

	def is_disk_io(self):
		return self.disk_io

