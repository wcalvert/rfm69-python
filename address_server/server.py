#!/usr/bin/env python

import SocketServer
from address_server_pb2 import *
from messages import *
import Adafruit_BBIO.GPIO as GPIO
from rfm69 import RFM69, RF69_433MHZ, RF69_868MHZ, RF69_915MHZ
import time
import struct
import json
from json import JSONEncoder

NODEID 				= 1     # unique for each node on same network
NETWORKID 			= 100   # the same on all nodes that talk to each other
# Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#FREQUENCY 			= RF69_433MHZ
#FREQUENCY 			= RF69_868MHZ
FREQUENCY 			= RF69_915MHZ
ENCRYPTKEY 			= "sampleEncryptKey" # exactly the same 16 characters/bytes on all nodes!
IS_RFM69HW 			= True  # uncomment only for RFM69HW! Leave out if you have RFM69W!
ACK_TIME 			= 30    # max # of ms to wait for an ack
promiscuousMode		= False # set to 'true' to sniff all packets on the same network
LED_PIN 			= "P9_11"

class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__

class AddressServerException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Lease(object):
	uid = 0
	address = 0
	network = 0
	ttl = 0
	startTime = 0
	state = IDLE
	def __init__(self, uid, address, network=None, ttl=None, startTime=None, state=IDLE):
		self.uid = uid
		self.address = address
		self.ttl = 3600
		self.startTime = int(time.time())

class TCPServer(SocketServer.BaseRequestHandler):
	ADDRESS_MIN = 1
	ADDRESS_MAX = 255
	TTL = 3600
	GRACEPERIOD = 10 # time allowed between offer_sent and request
	leases = []
	address = 1
	callback = None

	@classmethod
	def registerCallback(self, callback):
		self.callback = callback

	def handle(self):
		m = address_server_message()
		data = self.request.recv(1024)
		print "got client address: {}".format(self.client_address[0])
		try:
			m.ParseFromString(data)
		except:
			if self.callback is not None:
				#for lease in self.leases:
				self.callback(data)
		if m.ident != MAGIC_NUM:
			print "This is very bad, we were able to decode but the magic num is wrong"
		else:
			self.stateProcess(m)

	def stateProcess(self, m):
		if m.type == address_server_message.DISCOVER:
			addr = self.lowestFreeAddress()
			print "got discover from {}, offering address {}".format(m.uid, addr)
			self.request.sendall(Offer(addr, self.TTL).serialize())
			new_lease = Lease(m.uid, addr)
			new_lease.state = OFFER_SENT
			for lease in self.leases:
				if lease.address == addr:
					self.leases.remove(lease)
			self.leases.append(new_lease)
		elif m.type == address_server_message.OFFER:
			print "got offer - that's bad, there's another address server present..."
		elif m.type == address_server_message.REQUEST:
			for lease in self.leases:
				if lease.address == m.offered_address:
					if lease.state == OFFER_SENT:
						age = time.time() - lease.startTime
						print "age: {}".format(age)
						if age < self.GRACEPERIOD:
							self.request.sendall(Ack(m.uid).serialize())
							lease.state = ACK_SENT
						else:
							self.request.sendall(Nack(m.uid).serialize())
							self.leases.remove(lease)
					else:
						print "Request was received from {}, but lease is in wrong state".format(m.uid)
						self.request.sendall(Ack(m.uid).serialize())
		elif m.type == address_server_message.ACK:
			print "got ack - ignoring"
		elif m.type == address_server_message.NACK:
			print "got nack - ignoring"
		else:
			print "Got unsupported message type: {}".format(m.type)
	
	def lowestFreeAddress(self):
		addr_range = range(self.ADDRESS_MIN, self.ADDRESS_MAX)
		addr_range.remove(self.address)
		for lease in self.leases:
			# check age of lease and remove if greater than TTL
			age = time.time() - lease.startTime
			if age > self.TTL:
				self.leases.remove(lease)
			else:
				if lease.address in addr_range:
					addr_range.remove(lease.address)
		if len(addr_range) > 0:
			return addr_range[0]
		else:
			return None

def callbackExample(obj, data):
	print "Got data inside callback: {}".format(data)

class RFServer(object):
	LEASE_FILENAME = "leases.json"
	ADDRESS_MIN = 1
	ADDRESS_MAX = 255
	TTL = 3600
	GRACEPERIOD = 10 # time allowed between offer_sent and request
	leases = []
	address = 1
	callback = None

	def __init__(self):
		GPIO.setup(LED_PIN, GPIO.OUT)
		GPIO.output(LED_PIN, GPIO.LOW)
		self.radio = RFM69()
		self.radio.initialize(FREQUENCY,NODEID,NETWORKID)
		if IS_RFM69HW:
			self.radio.setHighPower(IS_RFM69HW) #only for RFM69HW!
		self.radio.encrypt(ENCRYPTKEY)
		self.radio.promiscuous(promiscuousMode)
		self.readLeaseFile()
		print "Listening at {} MHz".format(433 if FREQUENCY==RF69_433MHZ else (868 if FREQUENCY==RF69_868MHZ else 915))

	def Blink(self, PIN, DELAY_MS):
		GPIO.output(PIN, GPIO.HIGH)
		GPIO.output(PIN, GPIO.LOW)

	def serve_forever(self):
		ackCount = 0
		packetCount = 0
		try:
			while True:
				if self.radio.receiveDone():
					packetCount += 1
					data = struct.pack(len(self.radio.DATA)*'B', *self.radio.DATA)
					m = address_server_message()
					try:
						m.ParseFromString(data)
						print "got client address: {}, uid: {}, raw data: {}".format(self.radio.SENDERID, m.uid, self.radio.DATA)
					except:
						if self.callback is not None:
							self.callback(data)
					if m.ident != MAGIC_NUM:
						print "This is very bad, we were able to decode but the magic num is wrong"
					else:
						self.stateProcess(m)
					if self.radio.ACKRequested():
						theNodeID = self.radio.SENDERID
						self.radio.sendACK()
						ackCount += 1
						if ackCount % 3 == 0:
							s = "Pinging node {} - ACK...".format(theNodeID)
							# Send with one attempt only
							if self.radio.sendWithRetry(theNodeID, "ACK TEST", 8, 1):  
								s += " ok!"
							else:
								s+= " nothing"
							print s
					self.Blink(LED_PIN, .003)
		finally:
			self.writeLeaseFile()

	def writeLeaseFile(self):
		try:
			with open(self.LEASE_FILENAME, 'w') as f:
				f.write(json.dumps(self.leases, cls=MyEncoder))
		except:
			print "Lease file could not be written before shutting down"

	def readLeaseFile(self):
		data = None
		try:
			with open(self.LEASE_FILENAME, 'r') as f:
				data = f.read()
		except:
			print "Lease file not found - skipping"
		try:
			objs = json.loads(data)
			for obj in objs:
				self.leases.append(Lease(obj['uid'], obj['address'], obj['address'], obj['network'], 
					obj['ttl'], obj['startTime'], obj['state']))
		except:
			print "Error reading lease file"

	def stateProcess(self, m):
		if m.type == address_server_message.DISCOVER:
			addr = self.lowestFreeAddress()
			print "got discover from {}, offering address {}".format(m.uid, addr)
			#self.request.sendall(Offer(addr, self.TTL).serialize())
			new_lease = Lease(m.uid, addr)
			new_lease.state = OFFER_SENT
			for lease in self.leases:
				if lease.address == addr:
					self.leases.remove(lease)
			self.leases.append(new_lease)
		elif m.type == address_server_message.OFFER:
			print "got offer - that's bad, there's another address server present..."
		elif m.type == address_server_message.REQUEST:
			for lease in self.leases:
				if lease.address == m.offered_address:
					if lease.state == OFFER_SENT:
						age = time.time() - lease.startTime
						print "age: {}".format(age)
						if age < self.GRACEPERIOD:
							self.request.sendall(Ack(m.uid).serialize())
							lease.state = ACK_SENT
						else:
							self.request.sendall(Nack(m.uid).serialize())
							self.leases.remove(lease)
					else:
						print "Request was received from {}, but lease is in wrong state".format(m.uid)
						#self.request.sendall(Ack(m.uid).serialize())
		elif m.type == address_server_message.ACK:
			print "got ack - ignoring"
		elif m.type == address_server_message.NACK:
			print "got nack - ignoring"
		else:
			print "Got unsupported message type: {}".format(m.type)
	
	def lowestFreeAddress(self):
		addr_range = range(self.ADDRESS_MIN, self.ADDRESS_MAX)
		addr_range.remove(self.address)
		for lease in self.leases:
			# check age of lease and remove if greater than TTL
			age = time.time() - lease.startTime
			if age > self.TTL:
				self.leases.remove(lease)
			else:
				if lease.address in addr_range:
					addr_range.remove(lease.address)
		if len(addr_range) > 0:
			return addr_range[0]
		else:
			return None

def main():
	#host, port = "localhost", 9999
	#SocketServer.TCPServer.allow_reuse_address = True
	#server = SocketServer.TCPServer((host, port), TCPServer)
	#Server.registerCallback(callbackExample)
	#print "Listening on: {}:{}".format(host, port)
	#server.serve_forever()
	server = RFServer()
	server.serve_forever()


if __name__ == "__main__":
	main()
