class Payload:

	def __init__(self, initialDateTime, payloadID, size, lastModified, payloadData, roundTripTime):
		self.initialDateTime = initialDateTime
		self.payloadID = payloadID
		self.size = size
		self.lastModified = lastModified
		self.payloadData = payloadData
		self.roundTripTime = roundTripTime
