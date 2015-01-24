#!/usr/bin/env python

# Sample Moteino RFM69 Node sketch, with ACK and optional encryption
# Ported from Felix Rusu's original example code.

import Adafruit_BBIO.GPIO as GPIO
from rfm69 import rfm69
import time

NODEID				= 2    #unique for each node on same network
NETWORKID			= 100  #the same on all nodes that talk to each other
GATEWAYID			= 1
#Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#FREQUENCY			= rfm69.RF69_433MHZ
#FREQUENCY			= rfm69.RF69_868MHZ
FREQUENCY			= rfm69.RF69_915MHZ
ENCRYPTKEY			= "sampleEncryptKey" #exactly the same 16 characters/bytes on all nodes!
IS_RFM69HW			= True #uncomment only for RFM69HW! Leave out if you have RFM69W!
ACK_TIME			= 30 # max # of ms to wait for an ack
RETRIES				= 5
TRANSMITPERIOD		= 150 #transmit a packet to gateway so often (in ms)
payload				= "123 ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LED_PIN 			= "P9_11"

def main():
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN, GPIO.LOW)
	radio = rfm69.RFM69()
	radio.initialize(FREQUENCY,NODEID,NETWORKID)
	if IS_RFM69HW:
		radio.setHighPower(IS_RFM69HW) #uncomment only for RFM69HW!

	radio.encrypt(ENCRYPTKEY)
	print "Transmitting at {} Mhz...".format(433 if FREQUENCY==rfm69.RF69_433MHZ else (868 if FREQUENCY==rfm69.RF69_868MHZ else 915))
	
	lastPeriod = 0
	sendSize = 0

	while True:
		#check for any received packets
		if (radio.receiveDone()):
			print "[{}] {} [RX_RSSI: {}]".format(radio.SENDERID, radio.DATA, radio.RSSI)
			if (radio.ACKRequested()):
				radio.sendACK()
				print " - ACK sent"
				Blink(LED_PIN, .003)

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
			Blink(LED_PIN, .003)

def Blink(PIN, DELAY_MS):
	# Flicker will be visible even with no sleep.
	#time.sleep(DELAY_MS)
	GPIO.output(PIN, GPIO.HIGH)
	#time.sleep(DELAY_MS)
	GPIO.output(PIN, GPIO.LOW)

if __name__ == "__main__":
	main()