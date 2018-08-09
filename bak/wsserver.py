import asyncio
import websockets

CHECK_CHAR = '/checkChar'
CHECK_AVAIL_CHAR = '/checkAvailChar'
SET_CHAR ='/setChar/'
SET_DICE='/setDice/'
CHECK_CONN='/checkConnection'
RESET_ALL='/reset_all'
RESET='/reset'
PARTNER_MOVED='/partnerMoved'


class ScratchClient():
	charName = ''
	address = ()
	pendingAction = 0



class WSServer:
    charAssignment = {} # stores the character, and it's IP, pendingAction list; the key is the character name, e.g. 1/2/3...
    allChars = ('a','b','c')#all available chars for selection
    selectedChars =[] #a list to store selected chars
    movingCharIndex = 0 # the index of the char that is moving at the moment, pls note it's index, not the char itself



    def partnerMoved(self,path):
    	fromClient = path[14:15]#to split /partnerMoved/a/b
    	charMoved = path[16]

    	self.charAssignment[fromClient].pendingAction=0
    	print('partnerMoved',fromClient,charMoved)
    	self.movingCharIndex = self.movingCharIndex+1
    	if(self.movingCharIndex >= len(self.selectedChars)):
    		self.movingCharIndex = 0

    	#print('after partnerMoved:',self.selectedChars[self.movingCharIndex], self.charAssignment)

    	return self.selectedChars[self.movingCharIndex]


    def move(self,path):
    	steps = int(path[9]) # get how many steps to move in int
    	#
    	#for i in self.selectedChars: #add current action to all chars' (except the moving one) pending action list
    	#	if(i != self.selectedChars[self.movingCharIndex]):
    	self.charAssignment[self.selectedChars[self.movingCharIndex]].pendingAction=steps#set the moving steps of current char

    	return 'moved'



    def getAvailableChars(self):#return available characters like 1|2|
    	output = ''
    	for i in self.allChars:
    		if(i not in self.selectedChars):
    			output = output + str(i) + '|'
    	return output
    def getSelectedChars(self):#return available characters like 1|2|
    	output = ''
    	for i in self.selectedChars:
    		output = output + str(i) + '|'
    	return output

    def setChar(self,path):# assign a char according to the IP; return the selected chars after that, so that the client knows how many chars connected
    	char = path[9]
    	#print('setChar',self.client_address[0],char)
    	if(char in self.allChars):
    		aClient = ScratchClient()
    		aClient.charName = char
    		#aClient.address = self.client_address
    		self.charAssignment[char] = aClient
    		self.selectedChars.append(char)


    	return self.getSelectedChars()



    
        


    def reset(self):
    	print('empty reset')
    	self.charAssignment = {} # stores the character, and it's IP, pendingAction list; the key is the character name, e.g. 1/2/3...
    	self.allChars = ('a','b','c')#all available chars for selection
    	self.selectedChars =[] #a list to store selected chars
    	self.movingCharIndex = 0 # the index of the char that is moving at the moment, pls note it's index, not the char itself

    def startServer(self):
    	print('starting ws server')
    	start_server = websockets.serve(self.handler, '', 8765)
    	asyncio.get_event_loop().run_until_complete(start_server)
    	asyncio.get_event_loop().run_forever()



		


    async def consumer(self, websocket, message):# the real consumer
    	if(message == CHECK_AVAIL_CHAR):         
    	    print('now send:',message+'>'+self.getAvailableChars())
    	    await websocket.send(message+'>'+self.getAvailableChars())


    	elif(SET_CHAR in message):#sth like '/setChar/1'           
    	    #await websocket.send(message+'>'+self.setChar(message))
    	    self.setChar(message)
    	    print('handle setchar',self.selectedChars,len(self.selectedChars), len(self.connected))
    	    if(len(self.selectedChars)>1):#if more than one char selected, now can start the game, send moving char infor to all clients
    	    	for ws in self.connected:
    	    		await ws.send(SET_CHAR+'>'+self.getSelectedChars())
    	    		await ws.send(CHECK_CHAR+'>'+self.selectedChars[self.movingCharIndex]+' %s'%(self.charAssignment[self.selectedChars[self.movingCharIndex]].pendingAction))
    	    		
    		

    	elif(SET_DICE in message):#sth like '/setDice/3'
    	    self.move(message)
    	    for ws in self.connected:
    	    	await ws.send(CHECK_CHAR+'>'+self.selectedChars[self.movingCharIndex]+' %s'%(self.charAssignment[self.selectedChars[self.movingCharIndex]].pendingAction))
    	    		

    	    #await websocket.send(message+'>'+)
    	elif(PARTNER_MOVED in message):#sth like '/partnerMoved/a/b'
    	    self.partnerMoved(message)
    	    for ws in self.connected:
    	    	await ws.send(CHECK_CHAR+'>'+self.selectedChars[self.movingCharIndex]+' %s'%(self.charAssignment[self.selectedChars[self.movingCharIndex]].pendingAction))
    	    

    	elif(message == CHECK_CHAR):#return the moving char TODO
    	    await websocket.send(message+'>'+self.selectedChars[self.movingCharIndex]+' %s'%(self.charAssignment[self.selectedChars[self.movingCharIndex]].pendingAction))
    	elif(message == CHECK_CONN):# this is to update the moving char parm
    	    await websocket.send(message+'>'+self.getSelectedChars())

    	elif(message == RESET):# this is to reset
    	    self.reset()
		

    async def producer(self):
    	#await asyncio.sleep(5)
    	return ''


    async def consumer_handler(self,websocket, path):
        while True:
            message = await websocket.recv()
            print('consume', message)
            await self.consumer(websocket, message)

    async def producer_handler(self,websocket, path):
        pass
	    #while True:
	    #    message = await self.producer()
	    #    await websocket.send(message)

    connected = set()

	


	




    async def handler(self,websocket, path):
        #print('path',path)
        print(websocket.local_address)
        print(websocket.remote_address)
        # Register.
        self.connected.add(websocket)


	    
        try:
	        # Implement logic here.
            await asyncio.wait([self.singleHandler(ws,path) for ws in self.connected])
	        #await asyncio.sleep(10)
        finally:
	        # Unregister.
            self.connected.remove(websocket)

    async def singleHandler(self,websocket, path):
        consumer_task = asyncio.ensure_future(
            self.consumer_handler(websocket, path))
        producer_task = asyncio.ensure_future(
            self.producer_handler(websocket, path))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.ALL_COMPLETED,
        )
        for task in pending:
            task.cancel()



WSServer().startServer()



