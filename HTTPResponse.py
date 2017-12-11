class HTTPResponse():

	def __init__(self):
		self.http_version = 'HTTP/1.1'
		self.status_code = '200'
		self.reason_phrase = 'OK'
		self.status_line = self.http_version + ' ' + self.status_code + ' ' + self.reason_phrase + '\r\n' + '\r\n'
			
	def respond(self):
		return self.status_line
