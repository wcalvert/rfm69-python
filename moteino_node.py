#!/usr/bin/env python

# Sample Moteino RFM69 Node sketch, with ACK and optional encryption
# Ported from Felix Rusu's original example code.

from rfm69 import RFM69, RF69_433MHZ, RF69_868MHZ, RF69_915MHZ
import time

NODEID				= 2    #unique for each node on same network
NETWORKID			= 100  #the same on all nodes that talk to each other
GATEWAYID			= 1
#Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#FREQUENCY			= RF69_433MHZ
#FREQUENCY			= RF69_868MHZ
FREQUENCY			= RF69_915MHZ
ENCRYPTKEY			= "sampleEncryptKey" #exactly the same 16 characters/bytes on all nodes!
IS_RFM69HW			= True #uncomment only for RFM69HW! Leave out if you have RFM69W!
ACK_TIME			= 30 # max # of ms to wait for an ack
RETRIES				= 5
TRANSMITPERIOD		= 150 #transmit a packet to gateway so often (in ms)
payload				= "123 ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():
	radio = RFM69()
	radio.initialize(FREQUENCY,NODEID,NETWORKID)
	if IS_RFM69HW:
		radio.setHighPower(IS_RFM69HW) #uncomment only for RFM69HW!

	radio.encrypt(ENCRYPTKEY)
	print "Transmitting at {} Mhz...".format(433 if FREQUENCY==RF69_433MHZ else (868 if FREQUENCY==RF69_868MHZ else 915))
	
	lastPeriod = 0
	sendSize = 0

	while True:
		#check for any received packets
		if (radio.receiveDone()):
			print "[{}] {} [RX_RSSI: {}]".format(radio.SENDERID, radio.DATA, radio.RSSI)
			if (radio.ACKRequested()):
				radio.sendACK()
				print " - ACK sent"
				Blink(3,3)

		currPeriod = radio.millis()/TRANSMITPERIOD
		if (currPeriod != lastPeriod):
			lastPeriod = currPeriod
			s = "Sending[{}]: {} ".format(sendSize, payload[:sendSize])
			if (radio.sendWithRetry(GATEWAYID, payload, sendSize, retries=RETRIES, retryWaitTime=ACK_TIME)):
				s += "ok!"
			else:
				s += "nothing..."
			print s
			sendSize = (sendSize + 1) % 31
			Blink(3,3)

def Blink(PIN, DELAY_MS):
	pass

if __name__ == "__main__":
	main()