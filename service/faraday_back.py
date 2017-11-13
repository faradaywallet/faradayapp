#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import cc_crypt

class faraday_serv(BaseHTTPRequestHandler):
    ''' HTTP request handlers for Faraday Wallet application '''

    def do_headers(self):
        ''' Define headers '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        f = open('../view/index.html')  # Open main page
        self.do_headers()
        self.wfile.write(bytes(f.read(), 'utf-8'))
        return

    def do_POST(self):
        self.do_headers()
        content_length = int(self.headers.get('Content-Length', 0))
        raw_cc_num = self.rfile.read(content_length)

        # Parse credit card number from response
        cc_num = raw_cc_num.decode().split('creditCard=')[1]
        print(cc_num)

        # Encrypt cc_num
        enc_cc_num = cc_crypt.encrypt(secret_key, cc_num)
        # print (enc_cc_num)
        #
        # dec_cc_num = cc_crypt.decrypt(secret_key, enc_cc_num)
        # print (dec_cc_num)

        return

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=faraday_serv, port=8080):
    secret_key = cc_crypt.generate_key()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting connection...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
