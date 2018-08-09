
from wsserver import WSServer



class ScratchClient():
	charName = ''
	address = ()
	pendingAction = 0





class Tser:#this is the server to handle all scratch client requests



    def partnerMoved(self):
    	fromClient = self.path[14:15]#to split /partnerMoved/a/b
    	charMoved = self.path[16]

    	tser.charAssignment[fromClient].pendingAction=0
    	print('partnerMoved',fromClient,charMoved)
    	tser.movingCharIndex = tser.movingCharIndex+1
    	if(tser.movingCharIndex >= len(tser.selectedChars)):
    		tser.movingCharIndex = 0

    	print('after partnerMoved:',tser.selectedChars[tser.movingCharIndex], tser.charAssignment)

    	return tser.selectedChars[tser.movingCharIndex]


    def move(self):
    	steps = int(self.path[9]) # get how many steps to move in int
    	#
    	#for i in tser.selectedChars: #add current action to all chars' (except the moving one) pending action list
    	#	if(i != tser.selectedChars[tser.movingCharIndex]):
    	tser.charAssignment[tser.selectedChars[tser.movingCharIndex]].pendingAction=steps#set the moving steps of current char

    	return 'moved'



    def getAvailableChars(self):#return available characters like 1|2|
    	output = ''
    	for i in tser.allChars:
    		if(i not in tser.selectedChars):
    			output = output + str(i) + '|'
    	return output
    def getSelectedChars(self):#return available characters like 1|2|
    	output = ''
    	for i in tser.selectedChars:
    		output = output + str(i) + '|'
    	return output

    def setChar(self):# assign a char according to the IP; return the available chars after that
    	char = self.path[9]
    	print('setChar',self.client_address[0],char)
    	if(char in tser.allChars):
    		aClient = ScratchClient()
    		aClient.charName = char
    		aClient.address = self.client_address
    		tser.charAssignment[char] = aClient

    		tser.selectedChars.append(char)
    		
    	return self.getAvailableChars()



    def do_GET(self):
        print(self.path)
        


    def reset(self):
    	print('empty reset')
    	#tser.charAssignment = {} # stores the character, and it's IP, pendingAction list; the key is the character name, e.g. 1/2/3...
    	#tser.allChars = ('a','b','c')#all available chars for selection
    	#tser.selectedChars =[] #a list to store selected chars
    	#tser.movingCharIndex = 0 # the index of the char that is moving at the moment, pls note it's index, not the char itself



    def reply(self, strOut):# format and send out response
        self.send_response(200)
        self.end_headers()
        print('replying:',strOut)
        self.wfile.write(strOut.encode('UTF-8'))
    

    def log_message(self, format, *args):
        return

    def wsConsumer(self,message,path):
        print('wxConsumer:',message)
        if(self.path == '/checkAvailChar'):         
            self.reply(self.getAvailableChars())


        elif('/setChar/' in self.path):#sth like '/setChar/1'           
            self.reply(self.setChar())

        elif('/setDice/' in self.path):#sth like '/setDice/3'
            self.reply(self.move())
        elif('/partnerMoved/' in self.path):#sth like '/partnerMoved/a/b'
            self.reply(self.partnerMoved())
        elif(self.path == '/checkChar'):#return the moving char TODO
            self.reply(tser.selectedChars[tser.movingCharIndex]+' %s'%(tser.charAssignment[tser.selectedChars[tser.movingCharIndex]].pendingAction))
        elif(self.path == '/checkConnection'):# this is to update the moving char parm
            self.reply(self.getSelectedChars())

        elif(self.path == '/reset_all'):# this is to reset
            self.reset()

    def wsProducer(self):
        #nth
        return 'wsProducer'





tser = Tser()
tser.charAssignment = {} # stores the character, and it's IP, pendingAction list; the key is the character name, e.g. 1/2/3...
tser.allChars = ('a','b','c')#all available chars for selection
tser.selectedChars =[] #a list to store selected chars
tser.movingCharIndex = 0 # the index of the char that is moving at the moment, pls note it's index, not the char itself






ws = WSServer(tser.wsConsumer,tser.wsProducer)

ws.startServer()

