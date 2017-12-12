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
	def respond(response_code):
		valid_responses = [HTTP_200_OK, HTTP_302_NOT_MODIFIED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_SERVICE_UNAVAILABLE]
		if response_code not in valid_responses:
			print('Invalid Response Type')
			return 0
					
		if response_code == HTTP_200_OK:
			return HTTPResponse.get_response_type('200', 'OK')
		elif response_code == HTTP_302_NOT_MODIFIED:
			return HTTPResponse.get_response_type('302', 'NOT MODIFIED')
		elif response_code == HTTP_400_BAD_REQUEST:
			return HTTPResponse.get_response_type('400', 'BAD REQUEST')
		elif response_code == HTTP_404_NOT_FOUND:
			return HTTPResponse.get_response_type('404', 'NOT FOUND')
		else:
			return HTTPResponse.get_response_type('500', 'SERVICE UNAVAILABLE')

	@staticmethod
	def get_response_type(status_code, response_phrase):
		return (HTTPResponse.HTTP_VERSION + ' ' + status_code + ' ' + response_phrase + '\r\n' + '\r\n').encode('utf-8')
		
if __name__ == '__main__':
	print(HTTPResponse.respond(500)) # for test
