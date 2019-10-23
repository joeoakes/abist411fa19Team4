import json
import pymongo
import socket
import sys
from Agent import Agent
from Payload import Payload
from pymongo import MongoClient

import urllib.request

from Log import Log
from datetime import datetime

class Agent5(Agent):

	def __init__(self):
		self.agentID = '00005'

	def receiveAndStoreLog(self):
		try:
			# Create socket on localhost at port 8080, IPv4/TCP
			serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			serversocket.bind((socket.gethostname(), 8080))
			serversocket.listen(5)

			# Continuosly listen for connection
			# Convert received bytestream to JSON and print
			while True:
				print("Listening for connection...")
				clientsocket, address = serversocket.accept()
				print(f"Connection established from {address}")
				payload = clientsocket.recv(1024)

				print("Log request received")
				self.logRequest(payload)

				# decodedPayload = json.loads(payload.decode('utf-8'))
				# jsonPayload = json.dumps(decodedPayload)
				# print(jsonPayload)
				# print(type(jsonPayload))

		except Exception as e:
			print(e)

	def logRequest(self, log):

		try:
			decodedPayload = json.loads(log.decode('utf-8'))
			client = MongoClient('localhost', 27017)
			# print("Connected to MongoDB")
			db = client.ProjectDiamondLogs
			# print("Database Name: diamondLogs")
			collection = db.LogFiles
			# print("Collection Name: logs")
			post =  decodedPayload
			# print("Log request received")
			post_id = collection.insert_one(post)
			print("Log added")
		except Exception as e:
			print(e)


agent = Agent5()	
agent.receiveAndStoreLog()

