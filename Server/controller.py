import json
import base64
class Controller:
	def __init__(self, ws, ra):
		self.ws = ws
		self.ra = ra
		self.i = 0
	async def send_cmd(self, cmd):
		msg = {"type":"cmd", "data":cmd}
		msg = json.dumps(msg)
		await self.ws.send(msg)

	async def send_log(self, log):
		msg = {"type":"log", "data":log}
		msg = json.dumps(msg)
		await self.ws.send(msg)

	async def process_img(self, data):
		#print(base64.b64encode(data)
		await self.ws.send(base64.b64encode(data))

	def has_same_ra(self, ra):
		if ra[0] == self.ra[0] and ra[1] == self.ra[1]:
			return True
		else:
			return False
	def close(self):
		self.ws.close()
