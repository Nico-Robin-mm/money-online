import asyncio
import websockets


async def consumer(message):
	print('consume',message)

async def producer():
	out = 'msg22'
	print('produce',out)
	await asyncio.sleep(5)
	return out

async def consumer_handler(websocket):
    while True:
        message = await websocket.recv()
        await consumer(message)

async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)


async def handler():
	async with websockets.connect('ws://localhost:8765') as websocket:
		consumer_task = asyncio.ensure_future(consumer_handler(websocket))
		producer_task = asyncio.ensure_future(producer_handler(websocket))
		done, pending = await asyncio.wait([consumer_task, producer_task],return_when=asyncio.FIRST_COMPLETED,)
		for task in pending:
			task.cancel()

async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(handler())