# This class serves as an interface definition for any radio or simulator.

class BaseRadio(object):

	def __init__(self):
		pass

	def initialize(self, freqBand, nodeId, networkID):
		raise NotImplementedError

	def sleep(self):
		raise NotImplementedError

	def setAddress(self, addr):
		raise NotImplementedError

	def setNetwork(self, networkID):
		raise NotImplementedError

	def setPowerLevel(self, powerLevel):
		raise NotImplementedError

	def send(self, toAddress, buffer, bufferSize, requestACK):
		raise NotImplementedError

	def sendWithRetry(self, toAddress, buffer, bufferSize, retries=2, retryWaitTime=40):
		raise NotImplementedError

	def ACKReceived(self, fromNodeID):
		raise NotImplementedError 

	def ACKRequested(self):
		raise NotImplementedError

	def sendACK(self, buffer="", bufferSize=0):
		raise NotImplementedError

	def receiveDone(self):
		raise NotImplementedError

	def setEncryptionKey(self, key):
		raise NotImplementedError
