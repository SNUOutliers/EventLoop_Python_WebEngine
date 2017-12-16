import io
import glob
from event import Event


class HTTPParser:
	
	def __init__(self):
		self.method = ""
		self.request_uri = ""
		self.protocol = ""
		self.connection = ""
		
	def parse(self, request):
		''' This method turns HTTPRequset into Event and returns it. '''
		request_line = request.split('\r\n')[0]
		additional_info = request.split('\r\n')[1:]

		# 1. parsing request_line 
		parsed_rl = request_line.split(' ')

		if len(parsed_rl) == 3:
			self.method = parsed_rl[0]
			self.request_uri = parsed_rl[1]
			self.protocol = parsed_rl[2]

		# 2. parsing additional information
		#	general-header, request-header, entity-header
		#   especially, get 'Connection' info.
		info_dict = {}
#		print('Additional info: ' + str(additional_info))
		for info in additional_info:
			if ': ' not in info:
				continue
			key = info.split(': ')[0]
			value = info.split(': ')[1]
			info_dict[key] = value
		self.connection = info_dict['Connection']

		# Check whether data is inserted correctly
		print('Method: ' + self.method)
		print('Request-URI: ' + self.request_uri)
		print('HTTP-Version: ' + self.protocol)
		print('Connection: ' + self.connection)

		# Check whether requested uri needs disk_io or not.
		return Event(self.method, self.request_uri, disk_io=(self.request_uri != '/'))

	def get_connect_info(self):
		return self.connection

