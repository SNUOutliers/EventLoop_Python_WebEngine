from status import *

## HTTPReponse type ###
# HTTP_200_OK = 200
# HTTP_302_NOT_MODIFIED = 302
# HTTP_400_BAD_REQUEST = 400
# HTTP_404_NOT_FOUND = 404
# HTTP_500_SERVICE_UNAVAILABLE = 500

class HTTPResponse():
	HTTP_VERSION = 'HTTP/1.1'

	@staticmethod
	def respond(response_code, event):
		valid_responses = [HTTP_200_OK, HTTP_302_NOT_MODIFIED, HTTP_400_BAD_REQUEST, 
											 HTTP_404_NOT_FOUND, HTTP_500_SERVICE_UNAVAILABLE]
		if response_code not in valid_responses:
			print('Invalid Response Type')
			return 0
					
		if response_code == HTTP_200_OK:
			return HTTPResponse.get_response_type('200', 'OK', event)
		elif response_code == HTTP_302_NOT_MODIFIED:
			return HTTPResponse.get_response_type('302', 'NOT MODIFIED', event)
		elif response_code == HTTP_400_BAD_REQUEST:
			return HTTPResponse.get_response_type('400', 'BAD REQUEST', event)
		elif response_code == HTTP_404_NOT_FOUND:
			return HTTPResponse.get_response_type('404', 'NOT FOUND', event)
		else:
			return HTTPResponse.get_response_type('500', 'SERVICE UNAVAILABLE', event)

	@staticmethod
	def get_response_type(status_code, response_phrase, event):
		# 여기에는 Event에 대한 내용이 있어야 함.
		# Method에 대한 내용도 있어야 함.
		# 그래야 어떤 파일 읽을지 알게 됨.
#		f = open('./resources/example.html')
		message = event.response_bytes
		status_line = HTTPResponse.HTTP_VERSION + ' ' + status_code + ' ' + response_phrase + '\r\n' 
		
		entity_header = "Content-Length: " + str(len(message)) + "\n" + "Content-Type: " + event.content_type
		return (status_line + entity_header + '\r\n' + '\r\n').encode('utf-8') + message
		# 결국엔 encode 과정이 필요하게 됨!
		# 파일도 로컬에서 읽은 다음, encode하면 되지 않을까?!
