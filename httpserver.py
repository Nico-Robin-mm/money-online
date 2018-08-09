from http.server import HTTPServer, BaseHTTPRequestHandler
from wsserver import WSServer
import threading


class ScratchClient():
    charName = ''
    address = ()
    pendingAction = 0


def getSelectedChars():  # return available characters like 1|2|
    output = ''
    for i in httpd.selectedChars:
        output = output + str(i) + '|'
    return output


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):  # this is the server to handle all scratch client requests

    def partnerMoved(self):
        fromClient = self.path[14:15]  # to split /partnerMoved/a/b
        charMoved = self.path[16]

        httpd.charAssignment[fromClient].pendingAction = 0
        print('partnerMoved', fromClient, charMoved)
        httpd.movingCharIndex = httpd.movingCharIndex + 1
        if httpd.movingCharIndex >= len(httpd.selectedChars):
            httpd.movingCharIndex = 0

        print('after partnerMoved:', httpd.selectedChars[httpd.movingCharIndex], httpd.charAssignment)

        return httpd.selectedChars[httpd.movingCharIndex]

    def move(self):
        steps = int(self.path[9])  # get how many steps to move in int
        #
        # for i in httpd.selectedChars: #add current action to all chars' (except the moving one) pending action list
        #	if(i != httpd.selectedChars[httpd.movingCharIndex]):
        httpd.charAssignment[
            httpd.selectedChars[httpd.movingCharIndex]].pendingAction = steps  # set the moving steps of current char

        return 'moved'

    def getAvailableChars(self):  # return available characters like 1|2|
        output = ''
        for i in httpd.allChars:
            if i not in httpd.selectedChars:
                output = output + str(i) + '|'
        return output

    def setChar(self):  # assign a char according to the IP; return the available chars after that
        char = self.path[9]
        print('setChar', self.client_address[0], char)
        if char in httpd.allChars:
            aClient = ScratchClient()
            aClient.charName = char
            aClient.address = self.client_address
            httpd.charAssignment[char] = aClient

            httpd.selectedChars.append(char)

        return self.getAvailableChars()

    def do_GET(self):
        print(self.path)
        if self.path == '/checkAvailChar':
            self.reply(self.getAvailableChars())

        elif '/setChar/' in self.path:  # sth like '/setChar/1'
            self.reply(self.setChar())

        elif ('/setDice/' in self.path):  # sth like '/setDice/3'
            self.reply(self.move())
        elif ('/partnerMoved/' in self.path):  # sth like '/partnerMoved/a/b'
            self.reply(self.partnerMoved())
        elif (self.path == '/checkChar'):  # return the moving char TODO
            self.reply(httpd.selectedChars[httpd.movingCharIndex] + ' %s' % (
                httpd.charAssignment[httpd.selectedChars[httpd.movingCharIndex]].pendingAction))
        elif (self.path == '/checkConnection'):  # this is to update the moving char parm
            self.reply(getSelectedChars())

        elif (self.path == '/reset_all'):  # this is to reset
            self.reset()

    def reset(self):
        print('empty reset')

    # httpd.charAssignment = {} # stores the character, and it's IP, pendingAction list; the key is the character name, e.g. 1/2/3...
    # httpd.allChars = ('a','b','c')#all available chars for selection
    # httpd.selectedChars =[] #a list to store selected chars
    # httpd.movingCharIndex = 0 # the index of the char that is moving at the moment, pls note it's index, not the char itself

    def reply(self, strOut):  # format and send out response
        self.send_response(200)
        self.end_headers()
        print('replying:', strOut)
        self.wfile.write(strOut.encode('UTF-8'))

    def log_message(self, format, *args):
        return


httpd = HTTPServer(('localhost', 10000), SimpleHTTPRequestHandler)
httpd.charAssignment = {}  # stores the character, and it's IP, pendingAction list; the key is the character name,
# e.g. 1/2/3...
httpd.allChars = ('a', 'b', 'c')  # all available chars for selection
httpd.selectedChars = []  # a list to store selected chars
httpd.movingCharIndex = 0  # the index of the char that is moving at the moment, pls note it's index, not the char itself

threading.Thread(target=httpd.serve_forever).start()


def wsConsumer(message):
    print('wxConsumer:', message)


def wsProducer():
    print('wxProducer')
    return 'wsProducer'


ws = WSServer(wsConsumer, wsProducer)

ws.startServer()
