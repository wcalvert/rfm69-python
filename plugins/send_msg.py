import xmpp 
import datetime
import random

messages = ["WARNING: Failed PIN code entered at front door!",
"WARNING: Motion detected inside living room!",
"WARNING: Temperature has dropped below 60F!"]
message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S : ") + messages[random.randint(0, len(messages)-1)]

user="automation1982@gmail.com"
password="asfaf3453wtgsg423434234"
server=("talk.google.com", 5223)

jid = xmpp.JID(user) 
connection = xmpp.Client(jid.getDomain(), debug=[]) 
connection.connect(server) 
result = connection.auth(jid.getNode(), password ) 

connection.sendInitPresence()
connection.send(xmpp.Message("0gp4v4ldrqb7n29d4zkqc6uo2d@public.talk.google.com", message, typ="chat"))

connection.Process(1)
