#!/usr/bin/env python

import asyncio
import websockets
import json
import cv2
from PIL import Image
import numpy as np
import io
from client import Client
from controller import Controller

async def consumer(message):
	#print("< {}".format(message))
	pass
client = None
controller = None
train_mode = True
async def consumer_handler(websocket, path):
	global connected
	global client
	global controller
	global train_mode
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
				img = Image.open(io.BytesIO(img)).rotate(-90)
				imgByteArr = io.BytesIO()
				img.save(imgByteArr, format='JPEG')
				imgByteArr = imgByteArr.getvalue()
				if not train_mode:
					pass
				if controller != None:
					client.lastImg = img
					await controller.process_img(imgByteArr)

		elif data['mode'] == 'controller':
			#controller connection logic (only one client per session)
			if controller != None:
				if not controller.has_same_ra(ra):
					await controller.send_log("Closing connection")
					controller.close()
					controller = None
			if controller == None:
				controller = Controller(websocket, ra)
				await controller.send_log("hello created controller")
				print("created", ra)
			if client != None:
				if train_mode:
					await client.process_recvd_controller(data)
				else:
					await websocket.send("In Detection Mode")
			else:
				await websocket.send("client not connected")

		await consumer(message)

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
