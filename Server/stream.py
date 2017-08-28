#!/usr/bin/env python

import asyncio
import websockets
import json
from client import Client
import cv2
from PIL import Image
import numpy as np
import io

async def consumer(message):
	#print("< {}".format(message))
	pass
client = None
async def consumer_handler(websocket, path):
	global connected
	global client
	ra = websocket.remote_address
	while True:
		message = await websocket.recv()

		data = json.loads(message)

		if data['mode'] == 'client':
			#client connection logic (only one client per session)
			if client != None:
				if not client.has_same_ra(ra):
					await client.send_log("Closing connection")
					client.close()
					client = None
			if client == None:
				client = Client(websocket, ra)
				await client.send_log("hello created")
				print("created", ra)

			flag, img = client.process_recvd_client(data)
			if flag:
				Image.open(io.BytesIO(img)).rotate(-90).show()

		elif data['mode'] == 'controller':
			if client != None:
				await client.process_recvd_controller(data)
			else:
				await websocket.send("client not connected")
		await consumer(message)
	cv2.destroyWindow("preview")
async def handler(websocket, path):
	consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
	done, pending = await asyncio.wait(
		[consumer_task]
	)
	for task in pending:
		task.cancel()

start_server = websockets.serve(handler, '0.0.0.0', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
