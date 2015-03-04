from address_server_pb2 import *

# state definitions
IDLE = -1
DISCOVER_SENT = 0
DISCOVER_RECEIVED = 1
OFFER_SENT = 2
OFFER_RECEIVED = 3
REQUEST_SENT = 4
REQUEST_RECEIVED = 5
ACK_SENT = 6
ACK_RECEIVED = 7

# magic number to ident our protobuf messages
MAGIC_NUM = 0xfaf

class BaseMessage(object):
	def __init__(self):
		self.m = address_server_message()
		self.m.ident = MAGIC_NUM
	def serialize(self):
		return self.m.SerializeToString()

class Discover(BaseMessage):
	def __init__(self, uid):
		BaseMessage.__init__(self)
		self.m.type = address_server_message.DISCOVER
		self.m.uid = uid

class Offer(BaseMessage):
	def __init__(self, address, ttl):
		BaseMessage.__init__(self)
		self.m.type = address_server_message.OFFER
		self.m.offered_address = address
		self.m.ttl = ttl

class Request(BaseMessage):
	def __init__(self, uid, address):
		BaseMessage.__init__(self)
		self.m.type = address_server_message.REQUEST
		self.m.uid = uid
		self.m.offered_address = address

class Ack(BaseMessage):
	def __init__(self, uid):
		BaseMessage.__init__(self)
		self.m.type = address_server_message.ACK
		self.m.uid = uid

class Nack(BaseMessage):
	def __init__(self, uid):
		BaseMessage.__init__(self)
		self.m.type = address_server_message.NACK
		self.m.uid = uid
