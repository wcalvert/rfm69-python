#!/usr/bin/env python

# Sample Moteino RFM69 receiver/gateway sketch, with ACK and optional encryption
# Ported from Felix Rusu's original example code.

import Adafruit_BBIO.GPIO as GPIO
from radios import rfm69
import time
import struct

NODEID 				= 1     # unique for each node on same network
NETWORKID 			= 100   # the same on all nodes that talk to each other
# Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#FREQUENCY 			= rfm69.RF69_433MHZ
#FREQUENCY 			= rfm69.RF69_868MHZ
FREQUENCY 			= rfm69.RF69_915MHZ
ENCRYPTKEY 			= "sampleEncryptKey" # exactly the same 16 characters/bytes on all nodes!
IS_RFM69HW 			= True  # uncomment only for RFM69HW! Leave out if you have RFM69W!
ACK_TIME 			= 30    # max # of ms to wait for an ack
promiscuousMode		= False # set to 'true' to sniff all packets on the same network
LED_PIN 			= "P9_11"

def main():
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN, GPIO.LOW)
	radio = rfm69.RFM69()
	radio.initialize(FREQUENCY,NODEID,NETWORKID)
	if IS_RFM69HW:
		radio.setHighPower(IS_RFM69HW) #only for RFM69HW!
	radio.setEncryptionKey(ENCRYPTKEY)
	radio.setPromiscuous(promiscuousMode)
	print "Listening at {} MHz".format(433 if FREQUENCY==rfm69.RF69_433MHZ else (868 if FREQUENCY==rfm69.RF69_868MHZ else 915))

	ackCount = 0
	packetCount = 0
	while True:
		if radio.receiveDone():
			packetCount += 1
			data = struct.pack(len(radio.DATA)*'B', *radio.DATA)
			if not promiscuousMode:
				s = "#[{}][{}] {} [RX_RSSI:{}] {} bytes".format(packetCount, radio.SENDERID, data, radio.RSSI, len(radio.DATA))
			else:
				s = "#[{}][{}] to {} {} [RX_RSSI:{}]".format(packetCount, radio.SENDERID, radio.TARGETID, data, radio.RSSI)

			if radio.ACKRequested():
				theNodeID = radio.SENDERID
				radio.sendACK()
				s += " - ACK sent."
				print s

				# When a node requests an ACK, respond to the ACK
				# and also send a packet requesting an ACK (every 3rd one only)
				# This way both TX/RX NODE functions are tested on 1 end at the GATEWAY
				ackCount += 1
				if ackCount % 3 == 0:
					s = "Pinging node {} - ACK...".format(theNodeID)
					# Send with one attempt only
					if radio.sendWithRetry(theNodeID, "ACK TEST", 8, 1):  
						s += " ok!"
					else:
						s+= " nothing"
					print s
			Blink(LED_PIN, .003)

def Blink(PIN, DELAY_MS):
	# Flicker will be visible even with no sleep.
	#time.sleep(DELAY_MS)
	GPIO.output(PIN, GPIO.HIGH)
	#time.sleep(DELAY_MS)
	GPIO.output(PIN, GPIO.LOW)

if __name__ == "__main__":
	main()