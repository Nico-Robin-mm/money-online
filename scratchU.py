import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
import threading


CHECK_CHAR = '/checkChar'
CHECK_AVAIL_CHAR = '/checkAvailChar'
SET_CHAR ='/setChar/'
SET_DICE='/setDice/'
CHECK_CONN='/checkConnection'
RESET='/reset_all'
PARTNER_MOVED='/partnerMoved'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):


    

    def abcd(self):
        print('abcd')



    def updateMovingChar(self):#to update the moving char of this client, not server
        wsClient.sendMsg(self.path)   


    

    def updateAvailChar(self):
        print('updateAvailChar',wsClient)
        wsClient.sendMsg(self.path)

    

    def setChar(self):
        httpd.myChar = self.path[9]

        #print('setChar',self.getRes(self.path))
        wsClient.sendMsg(self.path)

    def move(self):#this should only be called by the current character's connector
        #print('move',self.getRes(self.path))
        wsClient.sendMsg(self.path)

    

    def checkConnection(self):
        wsClient.sendMsg(self.path)        
        #print('checkConnection',httpd.allConnected)

    def partnerMoved(self):
        wsClient.sendMsg(self.path+'/'+httpd.myChar+'/'+httpd.movingChar)
        '''the path is like /partnerMoved/a/b, where a is my own char, and b is the moving char
        this notify server who has moved, the response is the next moving char
        '''
        #print('partnerMoved',httpd.movingChar)

    def reset(self):
        httpd.availChar = 'x'
        httpd.myChar ='x'
        httpd.movingChar='x'
        httpd.allConnected=0
        httpd.dice =0

        wsClient.sendMsg(self.path)



    def do_GET(self):
        #print(self.client_address[0])
        if(self.path == '/poll'):
            output = 'Dice %s\ncharacter %s\nAllConnected %s\nAvailChar %s\n'%(httpd.dice,httpd.movingChar,httpd.allConnected,httpd.availChar)
         #   self.abcd()
            self.reply(output)
            #print (output)
        elif(self.path == CHECK_AVAIL_CHAR):#check avail chars
            self.updateAvailChar()
            self.reply('ok')
        elif(SET_CHAR in self.path):#sth like '/setChar/1'
            self.setChar()
            self.reply('ok')
        elif(SET_DICE in self.path):#sth like '/setDice/1'
            self.move()
            self.reply('ok')        
        elif(self.path == CHECK_CHAR):# this is to update the moving char parm
            self.updateMovingChar()
            self.reply('ok')
        elif(self.path == CHECK_CONN):# this is to update the moving char parm
            self.checkConnection()
            self.reply('ok')
        elif(self.path == RESET):# this is to reset
            self.reset()
            self.reply('ok')
        elif(self.path == PARTNER_MOVED):# this is to reset
            self.partnerMoved()
            self.reply('ok')

        elif(self.path == '/crossdomain.xml'):#TODO
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


class WSClient:


    websocket = None

    
        
        
    async def listen(self):
        async with websockets.connect('ws://10.0.2.2:8765') as websocket:
            self.websocket = websocket
            consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
            producer_task = asyncio.ensure_future(self.producer_handler(websocket))
            done, pending = await asyncio.wait([consumer_task, producer_task],return_when=asyncio.ALL_COMPLETED,)
            for task in pending:
                task.cancel()
        






    def sendMsg(self,msg):
        print('sendMsg', self.websocket)
        asyncio.new_event_loop().run_until_complete(self.websocket.send(msg))
        


    async def producer(self):
        print('pro')
        out = 'msg11'
        print('produce',out)
        await asyncio.sleep(5)
        return out

    async def consumer_handler(self,websocket):
        while True:
            message = await websocket.recv()
            await self.consumer(message)

    async def producer_handler(self,websocket):
        print('producer')
        
        #while True:
        #message = await self.producer()
        #await websocket.send(message)

    async def consumer(self,message):
        print('consume',message)
        if(message.startswith(CHECK_CHAR)):
            handle_updateMovingChar(message[len(CHECK_CHAR)+1])
        elif(message.startswith(CHECK_AVAIL_CHAR)):
            handle_updateAvailChar(message[len(CHECK_AVAIL_CHAR)+1:])
        elif(message.startswith(CHECK_CONN)):
            handle_checkConnection(message[len(CHECK_CONN)+1])
        elif(message.startswith(SET_CHAR)):
            handle_updateSelectedChar(message[len(CHECK_AVAIL_CHAR)+1:])#update the avail char param






def handle_updateMovingChar(res):
    httpd.movingChar = res[0:1]
    httpd.dice = res[2]
    print('update moving char',res)

def handle_updateAvailChar(res):
    httpd.availChar = res
    print('updateAvailChar',httpd.availChar)

def handle_checkConnection(res):
    httpd.allConnected=res

def handle_updateSelectedChar(res):
    httpd.allConnected=res

def handle_partnerMoved(res):
    httpd.movingChar = res#self.getRes(self.path+'/'+httpd.myChar+'/'+httpd.movingChar)
    


httpd = HTTPServer(('localhost', 12345), SimpleHTTPRequestHandler)
wsClient = WSClient()





httpd.availChar = 'x'
httpd.myChar ='x'
httpd.movingChar='x'
httpd.dice =0
httpd.allConnected=0

threading.Thread(target=httpd.serve_forever).start()
wsClient.loop = asyncio.get_event_loop()
wsClient.loop.run_until_complete(wsClient.listen())



