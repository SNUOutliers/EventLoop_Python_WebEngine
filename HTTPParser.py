import email
import pprint
import StringIO

class HTTPParser:
    @staticmethod
    def parse(request_string):
        # pop the first line so we only process headers
        _, headers = request_string.split('\r\n', 1)

        # construct a message from the request string
        message = email.message_from_file(StringIO.StringIO(headers))

        # construct a dictionary containing the headers
        headers = dict(message.items())

        # pretty-print the dictionary of headers
        pprint.pprint(headers, width=160)

        return headers