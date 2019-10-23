import json
import urllib.request
import uuid
import sys
import os
import socket
import ssl
import time
from Agent import Agent
from Payload import Payload
from Log import Log
from datetime import datetime
from pathlib import Path

class Agent1(Agent):

	def __init__(self):
		self.agentID = '00001'
		self.payload = Payload("", "", "", "", "", "")

	def curlJSONPayload(self):
		try:
			url = 'https://jsonplaceholder.typicode.com/posts/1/'
			req = urllib.request.urlopen(url)
			jsonBytes = req.read()

			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "curlJSONPayload", True)
			self.sendLog(log)

			return jsonBytes

		except urllib.error.HTTPError as e:
			print('Error retreiving payload.  Please check URL')
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "curlJSONPayload", False)
			self.sendLog(log)
		except Exception:
			print('An error occurred.')
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "curlJSONPayload", False)
			self.sendLog(log)

	def createPayload(self):
		try:
			payloadBytes = self.curlJSONPayload()
			decodedPayload = json.loads(payloadBytes.decode('utf-8'))
			jsonPayload = json.dumps(decodedPayload)

			initialDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			payloadID = str(uuid.uuid1())
			size = sys.getsizeof(payloadBytes)
			lastModified = initialDateTime
			payloadData = jsonPayload
			roundTripTime = None
			payload = Payload(initialDateTime, payloadID, size, lastModified, payloadData, roundTripTime)
			
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "createPayload", True)
			self.sendLog(log)

			return payload
		except Exception:
			print('Error creating payload.')
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "createPayload", False)
			self.sendLog(log)

	def setPayload(self):
		try:
			self.payload = self.createPayload()

			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "setPayload", True)
			self.sendLog(log)
		except Exception:
			print('Error setting payload.')
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "setPayload", False)
			self.sendLog(log)

	def saveJSONPayload(self):
		try:
			payload = self.payload
			payloadDetails = ""

			initialDateTime = payload.initialDateTime
			payloadID = payload.payloadID
			size = payload.size
			lastModified = payload.lastModified
			payloadData = payload.payloadData

			payloadDetails += '---------------------------'
			payloadDetails += os.linesep
			payloadDetails += 'ID: ' + str(payloadID)
			payloadDetails += os.linesep
			payloadDetails += 'Time: ' + initialDateTime
			payloadDetails += os.linesep
			payloadDetails += 'Size: ' + str(size) + ' Bytes'
			payloadDetails += os.linesep
			payloadDetails += 'Data:'
			payloadDetails += os.linesep
			payloadDetails += payloadData
			payloadDetails += os.linesep
			payloadDetails += '---------------------------'

			with open('../PayloadData/rawPayloads.txt', 'a') as outFile:
				jsonObjCurl = outFile.write(payloadDetails)

			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "saveJSONPayload", True)
			self.sendLog(log)	

		except FileNotFoundError:
			print('Save location not found.  Check PayloadData directory exists in ProjectDiamond package.')
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "saveJSONPayload", False)
			self.sendLog(log)
		except Exception:
			print('Error saving JSON payload.')	
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "saveJSONPayload", False)
			self.sendLog(log)

	def sendPayloadTLS(self):

		try:

			payload = self.payload
			jsonPayload = json.dumps(payload.__dict__).encode()
			print("Agent1 connecting on port 8080 using SSL...")
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ssl_sock = ssl.wrap_socket(s,
				ca_certs="../SSLCert/server.crt",
				cert_reqs=ssl.CERT_REQUIRED)
			ssl_sock.connect(('localhost', 8080))
			ssl_sock.sendall(jsonPayload)
			ssl_sock.close()

			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "sendPayloadTLS", True)
			self.sendLog(log)

		except Exception as e:
			print(e)
			log = self.createLog(self.agentID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "sendPayloadTLS", False)
			self.sendLog(log)

	def receiveRabbitMQ(self):
		print('TODO: Receive via RabbitMQ code...')

	def displayRTT(self):
		print('TODO: display RTT code...')

agent = Agent1()

agent.setPayload()
agent.saveJSONPayload()
agent.sendPayloadTLS()
time.sleep(15)
agent.setPayload()
agent.saveJSONPayload()
agent.sendPayloadTLS()
time.sleep(15)
agent.setPayload()
agent.saveJSONPayload()
agent.sendPayloadTLS()

