#!/usr/bin/env python

import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs

HOST_NAME = ''
PORT_NUMBER = 9000


def query_processing(query):
    if not ('value' in query and 'terms' in query):
        return {'status': 400, 'message': '''Both 'value' and 'terms' get parameters provided'''}

    elif query['terms'] <= 0:
        return {'status': 400, 'message': '''''terms' param should be a positive int'''}

    elif query['value'] <= 1:
        return {'status': 200, 'message': 'Fib sequence: %s' % query['value']}

    else:
        value = int(query['value'][0])
        terms = int(query['terms'][0])
        fib_sequence = list()

        fib = lambda n: fib(n - 1) + fib(n - 2) if n > 2 else 1

        for term in range(value, value + terms):
            fib_sequence.append(str(fib(term)))

        return {'status': 200, 'message': 'Fib sequence: %s' % ", ".join(fib_sequence)}


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        query = parse_qs(urlparse(s.path).query)
        fib_processing = query_processing(query)

        s.send_response(fib_processing['status'])
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Fib seq</title></head>")
        s.wfile.write("<body><p>%s</p>" % fib_processing['message'])
        s.wfile.write("</body></html>")


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)