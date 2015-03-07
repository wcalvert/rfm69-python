from yapsy.IPlugin import IPlugin
from firebase import Firebase
from firebase_token_generator import create_token
import time
import random
import yaml

messages = ["WARNING: Failed PIN code entered at front door!",
"WARNING: Motion detected inside living room!",
"WARNING: Temperature has dropped below 60F!"]

document = """firebase_url: https://your_acct.firebaseio.com/
data_bucket: automation
secret: your_secret"""

secrets_filename = "firebase_secrets.txt"

class FirebasePlugin(IPlugin):

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
			self._firebase_url = conf["firebase_url"]
			self._secret = conf["secret"]
			self._data_bucket = conf["data_bucket"]
		except:
			raise Exception("Error parsing {}!".format(secrets_filename))
		if self._firebase_url is None or self._secret is None:
			raise Exception("Error parsing {} - not all fields have been filled in!".format(secrets_filename))
		auth_payload = {"uid": "1", "auth_data": "foo", "other_auth_data": "bar"}
		token = create_token(self._secret, auth_payload)
		self._client = Firebase(self._firebase_url + self._data_bucket, auth_token=token)

	def process_message(self):
		message = messages[random.randint(0, len(messages)-1)]
		self._client.push({'timestamp': int(time.time()), 'message': message})
