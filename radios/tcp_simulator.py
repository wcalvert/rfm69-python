# **********************************************************************************
# Wes Calvert, 2015
# **********************************************************************************
# License
# **********************************************************************************
# This program is free software; you can redistribute it 
# and/or modify it under the terms of the GNU General    
# Public License as published by the Free Software       
# Foundation; either version 2 of the License, or        
# (at your option) any later version.                    
#                                                        
# This program is distributed in the hope that it will   
# be useful, but WITHOUT ANY WARRANTY; without even the  
# implied warranty of MERCHANTABILITY or FITNESS FOR A   
# PARTICULAR PURPOSE.  See the GNU General Public        
# License for more details.                              
#                                                        
# You should have received a copy of the GNU General    
# Public License along with this program; if not, write 
# to the Free Software Foundation, Inc.,                
# 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#                                                        
# Licence can be viewed at                               
# http:#www.fsf.org/licenses/gpl.txt                    
#
# Please maintain this license information along with authorship
# and copyright notices in any redistribution of this code
# **********************************************************************************

import gevent
from gevent import socket
from Crypto.Cipher import AES
from Crypto import Random
from base_radio import BaseRadio

class TCPSimulator(BaseRadio):
	# We do software AES encryption using these params
	_key = None
	_mode = AES.MODE_CFB

	# These are TCP server and client params
	_address = 'localhost'
	_port = 10000
	_ServerMode = False
	_server = None
	_client =None

	# These params are more for emulating the real radio
	_frequency = None
	_node = None
	_network = None
	_promiscuous = False
	_data = None

	def initialize(self, frequency, node, network):
		self._frequency = frequency
		self._node = node
		self._network = network

	def SetEncryptionKey(self, key):
		if len(key) != 16:
			raise Exception("Key must be exactly 16 bytes!")
		self._key = key

	# This initialize method is not going to be present in BaseRadio or in the real
	# radio class. We need a way to do TCP-specific setup.
	def TCPInitialize(self, ServerMode, address, port):
		self._ServerMode = ServerMode
		self._address = address
		self._port = port
		if(self._ServerMode):
			self._server = socket.socket()
			self._server.bind((self._address, self._port))
			self._server.listen(500)
		else:
			self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._client.connect((self._address, self._port))

	def ReceiveDone(self):
		try:
			sock, addr = self._server.accept()
			gevent.spawn(self.HandleSocket, sock, addr)
		except Exception as e:
			print e

	def HandleSocket(self, sock, addr):
		temp = sock.makefile().readline()
		#print "Just received: {}, key is now: {}".format(self.toHex(temp), self.toHex(self._key))
		#print "Temp is {} bytes".format(len(temp))
		if self._key is not None:
			#temp = temp.decode("hex")
			iv = temp[:16]
			data = temp[16:]
			decryptor = AES.new(self._key, self._mode, IV=iv)
			self._data = decryptor.decrypt(data)
		else:
			self._data = temp
		print "Got data: {}".format(self._data)
		sock.close()

	def SendWithRetry(self, toAddress, buffer, bufferSize, retries=2, retryWaitTime=40):
		pass

	def Send(self, toAddress, buffer, bufferSize, requestACK):
		if self._key is not None:
			while (len(buffer)+16) % 16 != 0:
				buffer += " "
			iv = Random.new().read(16)
			encryptor = AES.new(self._key, self._mode, IV=iv)
			buffer = iv + encryptor.encrypt(buffer)
		if self._ServerMode:
			pass
		else:
			print "About to send: {}".format(self.toHex(buffer))
			self._client.sendall(buffer)

	def toHex(self, s):
		return ":".join("{:02x}".format(ord(c)) for c in s)

if __name__ == "__main__":
	sim = TCPSimulator()
	sim.TCPInitialize(True, 'localhost', 10000)
	sim.SetEncryptionKey("MySampleKey12345")
	print "Now waiting for clients on port 10000 ..."
	while True:
		sim.ReceiveDone()