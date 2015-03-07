from yapsy.IPlugin import IPlugin
from twilio.rest import TwilioRestClient
import yaml
import random

messages = ["WARNING: Failed PIN code entered at front door!",
"WARNING: Motion detected inside living room!",
"WARNING: Temperature has dropped below 60F!"]

document = """twilio_sid: your_twilio_sid
twilio_token: your_twilio_token
twilio_number: your_twilio_sending_number
destination_number: your_phone_number"""

secrets_filename = "sms_secrets.txt"

class SmsPlugin(IPlugin):

	def __init__(self):
		try:
			with open(secrets_filename, "r") as f:
				data = f.read()
		except:
			err = "Error processing {} - make sure to fill in {}!".format(secrets_filename, secrets_filename)
			with open(secrets_filename, "w") as f:
				f.write(document)
			raise Exception(err)
		try:
			conf = yaml.load(data)
			self.twilio_sid = conf["twilio_sid"]
			self.twilio_token = conf["twilio_token"]
			self.twilio_number = conf["twilio_number"]
			self.destination_number = conf["destination_number"]
		except:
			raise Exception("Error parsing {}!".format(secrets_filename))
		self.client = TwilioRestClient(self.twilio_sid, self.twilio_token)
		if self.twilio_sid is None or self.twilio_token is None or self.destination_number is None or self.twilio_number is None:
			raise Exception("Error parsing {} - not all fields have been filled in!".format(secrets_filename))

	def process_message(self):
		message = messages[random.randint(0, len(messages)-1)]
		m = self.client.messages.create(to=self.destination_number, from_=self.twilio_number, body=message)