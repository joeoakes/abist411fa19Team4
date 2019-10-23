import json
import socket
import ssl
from Agent import Agent
from Payload import Payload
from Log import Log
from datetime import datetime


class Agent2(Agent):

	def __init__(self):
		self.agentID = '00002'
		self.payload = Payload("", "", "", "", "", "")

	def receivePayloadTLS(self):

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ssl_sock = ssl.wrap_socket(s,
				server_side=True,
				certfile="../SSLCert/server.crt",
				keyfile="../SSLCert/server.key")
			ssl_sock.bind(('localhost', 8080))
			ssl_sock.listen(5)

			while True:
				print('Listening for connections...')
				(clientsocket, address) = ssl_sock.accept()
				print(f"Connection established from {address}")
				payload = clientsocket.recv(1024)
				decodedPayload = json.loads(payload.decode('utf-8'))
				jsonPayload = json.dumps(decodedPayload)

				log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "receivePayloadTLS", True)
				self.sendLog(log)

		except Exception as e:
			print(e)
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "receivePayloadTLS", False)
			self.sendLog(log)



	def hashPayload(self):
		print('TODO: Hash payload code...')

	def sendPayloadSFTP(self):
		print('TODO: Send via SFTP code...')


agent = Agent2()
agent.receivePayloadTLS()