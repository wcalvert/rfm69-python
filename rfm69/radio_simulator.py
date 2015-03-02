#!/usr/bin/env python

from tcp_simulator import TCPSimulator
import socket

if __name__ == "__main__":
	r = TCPSimulator()
	r.TCPInitialize(False, "localhost", 10000)
	r.SetEncryptionKey("MySampleKey12345")
	r.Send(toAddress=None, buffer="Y HELO THAR", bufferSize=0, requestACK=False)