import socket
import sys
import time
from messages import *

HOST, PORT = "localhost", 9999
uid = 'dingleberry'

def sendDataGetResponse(data):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		sock.sendall(data)
		response = None
		while response is None:
			response = sock.recv(1024)
		return response
	finally:
		sock.close()

def sendData(data):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		sock.sendall(data)
	finally:
		sock.close()

def main():
	data = sendDataGetResponse(Discover(uid).serialize())
	m = address_server_message()
	m.ParseFromString(data)
	print m
	if m.type == address_server_message.OFFER:
		print "Got offer for address {}, sending request...".format(m.offered_address)
		#print "sleeping 15"
		#time.sleep(15)
		data = sendDataGetResponse(Request(uid, m.offered_address).serialize())
		m = address_server_message()
		m.ParseFromString(data)
		print m
		sendData("asdjfa;lksdjf")


if __name__ == "__main__":
	main()
	print "finished"
	#sendData("asdjfa;lksdjf")
	#sendData("asdjfa;235234")
	#sendData("dsfgghhlksdjf")