import socket
import json
from abc import ABC, abstractmethod
from datetime import datetime
from Log import Log

class Agent(ABC):

	@abstractmethod
	def __init__(self, agentID, payload):
		self.agentID = agentID
		self.payload = payload

	def createLog(self, originatingAgent, timestamp, currentProcess, processSuccess):
		log = Log(originatingAgent, timestamp, currentProcess, processSuccess)
		return log

	def sendLog(self, log):
		try:
			jsonPayload = json.dumps(log.__dict__)
			jsonPayload = jsonPayload.encode()
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((socket.gethostname(), 8080))
			clientsocket.sendall(jsonPayload)
			clientsocket.close()
		except Exception as e:
			print(e)
