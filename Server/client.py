import json
import base64
class Client:
	def __init__(self, ws, ra):
		self.ws = ws
		self.ra = ra
		self.i = 0
		self.lastImg = None
		self.controllCmds = ['fwd', 'left', 'right', 'bwd', 'off']

	async def send_cmd(self, cmd):
		msg = {"type":"cmd", "data":cmd}
		msg = json.dumps(msg)
		if cmd in self.controllCmds :
			self.saveTrainImg(cmd)
		await self.ws.send(msg)

	async def send_log(self, log):
		msg = {"type":"log", "data":log}
		msg = json.dumps(msg)
		await self.ws.send(msg)

	def process_recvd_client(self, data):
		if data['type'] == 'log':
			print(data['data'])
		elif data['type'] == 'img':
			#f = open(str(self.i)+'fname.jpg','bw')
			#self.i = self.i + 1
			im = base64.b64decode(data['data'])
			#f.write(im)
			#f.close()
			return (True, im)
		else:
			print("unknown type")
		return (False, None)
	def saveTrainImg(self, cmd):
		self.i = self.i+1
		self.lastImg.save("data/"+cmd+"/"+str(self.i)+".jpg", format='JPEG')

	async def process_recvd_controller(self, data):
		if data['type'] == 'log':
			await self.send_log(data['data'])
		elif data['type'] == 'cmd':
			await self.send_cmd(data['data'])
		else:
			print("unknown type")

	def has_same_ra(self, ra):
		if ra[0] == self.ra[0] and ra[1] == self.ra[1]:
			return True
		else:
			return False
	def close(self):
		self.ws.close()
