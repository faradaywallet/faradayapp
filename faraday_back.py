#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

class faraday_serv(BaseHTTPRequestHandler):
    ''' HTTP request handlers for Faraday Wallet application '''
    def do_headers(self):
        ''' Define headers '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        f = open('view/index.html')  # Open main page
        self.do_headers()
        self.wfile.write(bytes(f.read(), 'utf-8'))
        return

    def do_POST(self):
        self.do_headers()
        #print(self.headers)
        content_length = int(self.headers.get('Content-Length', 0))
        raw_cc_num = self.rfile.read(content_length)

        # Parse credit card number from response
        cc_num = raw_cc_num.decode().split('creditCard=')[1]
        return

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=faraday_serv, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting connection...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
