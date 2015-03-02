class BaseRadio(object):

	def __init__(self):
		pass

	def Initialize(self, frequency, node, network):
		pass

	def SetHighPower(self, HighPower):
		pass

	def SetEncryptionKey(self, key):
		pass

	def SetPromiscuousMode(self, mode):
		pass

	def GetSenderId(self):
		pass

	def GetData(self):
		pass

	def SendAck(self):
		pass

	def AckRequested(self):
		pass

	def ReceiveDone(self):
		pass

	def SendWithRetry(self, toAddress, buffer, bufferSize, retries=2, retryWaitTime=40):
		pass

	def Send(self, toAddress, buffer, bufferSize, requestACK):
		pass