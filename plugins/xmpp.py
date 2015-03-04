from yapsy.IPlugin import IPlugin
import xmpp 
import datetime
import random
import yaml

messages = ["WARNING: Failed PIN code entered at front door!",
"WARNING: Motion detected inside living room!",
"WARNING: Temperature has dropped below 60F!"]

document = """automation_user: dummy_acct@gmail.com
automation_password: dummy_acct_password
automation_server: talk.google.com
automation_port: 5223
destination_user: fill_me_in@public.talk.google.com"""

secrets_filename = "xmpp_secrets.txt"

class XmppPlugin(IPlugin):

	def __init__(self):
		try:
			with open(secrets_filename, "r") as f:
				data = f.read()
		except:
			err = "Error processing {} - make sure to fill in {} and reading the " + \
				"instructions in discover_gchat_id.py".format(secrets_filename, secrets_filename)
			with open(secrets_filename, "w") as f:
				f.write(document)
			raise Exception(err)
		try:
			conf = yaml.load(data)
			self.automation_user = conf["automation_user"]
			self.automation_password = conf["automation_password"]
			self.automation_server = conf["automation_server"]
			self.automation_port = conf["automation_port"]
			self.destination_user = conf["destination_user"]
		except:
			raise Exception("Error parsing {}!".format(secrets_filename))
		if self.automation_user is None or self.automation_password is None or self.automation_server is None or \
			self.automation_port is None or self.destination_user is None:
			raise Exception("Error parsing {} - not all fields have been filled in!".format(secrets_filename))
		server = (self.automation_server, self.automation_port)
		jid = xmpp.JID(self.automation_user) 
		self.connection = xmpp.Client(jid.getDomain(), debug=[]) 
		self.connection.connect(server) 
		result = self.connection.auth(jid.getNode(), self.automation_password) 
		self.connection.sendInitPresence()

	def process_message(self):
		message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S : ") + messages[random.randint(0, len(messages)-1)]
		self.connection.send(xmpp.Message(self.destination_user, message, typ="chat"))
		self.connection.Process(1)
