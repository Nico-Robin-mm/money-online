from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    charAssignment = []

    def abcd(self):
        print('abcd')

    def do_GET(self):
        print(self.client_address[0])
        if(self.path == '/poll'):
         #   self.abcd()
            self.replyA(b'Dice 4\ncharacter cat\nAllConnected 1\n')
        elif(self.path == '/crossdomain.xml'):
        	print('cod');
        	self.send_response(200)
        	self.end_headers()
        	self.wfile.write(b'<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"12345\"/></cross-domain-policy>')
        	self.wfile.write(b'\x00')

    def replyA(self, binOut):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(binOut)
    

    def log_message(self, format, *args):
        return


httpd = HTTPServer(('localhost', 12345), SimpleHTTPRequestHandler)
httpd.serve_forever()