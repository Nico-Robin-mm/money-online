from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    

    def abcd(self):
        print('abcd')

    def updateMovingChar(self):
        httpres = self.getRes(self.path)
        
        httpd.movingChar = httpres[0:1]
        httpd.dice = httpres[2]
        print('update moving char',httpres)


    def getRes(self, req):
        conn = HTTPConnection("localhost",10000)
        conn.request("GET",req)
        res = conn.getresponse()
        data = None
        if(res.status == 200):
            data = res.read().decode('UTF-8')
            print(data)
        conn.close()
        return data

    def updateAvailChar(self):

        httpd.availChar = self.getRes(self.path)
        print('updateAvailChar',httpd.availChar)

    def setChar(self):
        httpd.myChar = self.path[9]
        print('setChar',self.getRes(self.path))

    def move(self):#this should only be called by the current character's connector
        print('move',self.getRes(self.path))

    def checkConnection(self):
        httpd.allConnected=self.getRes(self.path)
        #print('checkConnection',httpd.allConnected)

    def partnerMoved(self):
        httpd.movingChar = self.getRes(self.path+'/'+httpd.myChar+'/'+httpd.movingChar)
        '''the path is like /partnerMoved/a/b, where a is my own char, and b is the moving char
        this notify server who has moved, the response is the next moving char
        '''
        print('partnerMoved',httpd.movingChar)

    def reset(self):
        httpd.availChar = 'x'
        httpd.myChar ='x'
        httpd.movingChar='x'
        httpd.allConnected=0
        httpd.dice =0

        self.getRes(self.path)



    def do_GET(self):
        #print(self.client_address[0])
        if(self.path == '/poll'):
            output = 'Dice %s\ncharacter %s\nAllConnected %s\nAvailChar %s\n'%(httpd.dice,httpd.movingChar,httpd.allConnected,httpd.availChar)
         #   self.abcd()

            self.reply(output)
            #print (output)
        elif(self.path == '/checkAvailChar'):
            self.updateAvailChar()
        elif('/setChar/' in self.path):#sth like '/setChar/1'
            self.setChar()
        elif('/setDice/' in self.path):#sth like '/setDice/1'
            self.move()
        
        elif(self.path == '/checkChar'):# this is to update the moving char parm
            self.updateMovingChar()
        elif(self.path == '/checkConnection'):# this is to update the moving char parm
            self.checkConnection()
        elif(self.path == '/reset_all'):# this is to reset
            self.reset()
        elif(self.path == '/partnerMoved'):# this is to reset
            self.partnerMoved()

        elif(self.path == '/crossdomain.xml'):
        	print('cod');
        	self.send_response(200)
        	self.end_headers()
        	self.wfile.write(b'<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"12345\"/></cross-domain-policy>')
        	self.wfile.write(b'\x00')

    def reply(self, strOut):# format and send out response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(strOut.encode('UTF-8'))
    

    def log_message(self, format, *args):
        return



httpd = HTTPServer(('localhost', 12345), SimpleHTTPRequestHandler)
httpd.availChar = 'x'
httpd.myChar ='x'
httpd.movingChar='x'
httpd.dice =0
httpd.allConnected=0
httpd.serve_forever()