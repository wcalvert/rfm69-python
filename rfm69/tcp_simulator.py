import gevent
from gevent import socket
from Crypto.Cipher import AES
from Crypto import Random
from base_radio import BaseRadio

class TCPSimulator(BaseRadio):
	# We do software AES encryption using these params
	__key = None
	__mode = AES.MODE_CFB

	# These are TCP server and client params
	__address = 'localhost'
	__port = 10000
	__ServerMode = False
	__server = None
	__client =None

	# These params are more for emulating the real radio
	__frequency = None
	__node = None
	__network = None
	__promiscuous = False
	__data = None

	def Initialize(self, frequency, node, network):
		self.__frequency = frequency
		self.__node = node
		self.__network = network

	def SetEncryptionKey(self, key):
		if len(key) != 16:
			raise Exception("Key must be exactly 16 bytes!")
		self.__key = key

	# This initialize method is not going to be present in BaseRadio or in the real
	# radio class. We need a way to do TCP-specific setup.
	def TCPInitialize(self, ServerMode, address, port):
		self.__ServerMode = ServerMode
		self.__address = address
		self.__port = port
		if(self.__ServerMode):
			self.__server = socket.socket()
			self.__server.bind((self.__address, self.__port))
			self.__server.listen(500)
		else:
			self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.__client.connect((self.__address, self.__port))

	def ReceiveDone(self):
		try:
			sock, addr = self.__server.accept()
			gevent.spawn(self.HandleSocket, sock, addr)
		except Exception as e:
			print e

	def HandleSocket(self, sock, addr):
		temp = sock.makefile().readline()
		#print "Just received: {}, key is now: {}".format(self.toHex(temp), self.toHex(self.__key))
		#print "Temp is {} bytes".format(len(temp))
		if self.__key is not None:
			#temp = temp.decode("hex")
			iv = temp[:16]
			data = temp[16:]
			decryptor = AES.new(self.__key, self.__mode, IV=iv)
			self.__data = decryptor.decrypt(data)
		else:
			self.__data = temp
		print "Got data: {}".format(self.__data)
		sock.close()

	def SendWithRetry(self, toAddress, buffer, bufferSize, retries=2, retryWaitTime=40):
		pass

	def Send(self, toAddress, buffer, bufferSize, requestACK):
		if self.__key is not None:
			while (len(buffer)+16) % 16 != 0:
				buffer += " "
			iv = Random.new().read(16)
			encryptor = AES.new(self.__key, self.__mode, IV=iv)
			buffer = iv + encryptor.encrypt(buffer)
		if self.__ServerMode:
			pass
		else:
			print "About to send: {}".format(self.toHex(buffer))
			self.__client.sendall(buffer)

	def toHex(self, s):
		return ":".join("{:02x}".format(ord(c)) for c in s)

if __name__ == "__main__":
	sim = TCPSimulator()
	sim.TCPInitialize(True, 'localhost', 10000)
	sim.SetEncryptionKey("MySampleKey12345")
	print "Now waiting for clients on port 10000 ..."
	while True:
		sim.ReceiveDone()