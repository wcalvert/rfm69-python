# ------------------------------------------
#                Instructions
# ------------------------------------------
# 0. As of 26 Feb 2015, I recommend installing the xmpppy module located here: https://github.com/ArchipelProject/xmpppy
#    It seems to actively maintained and some bugs have been fixed.
# 1. Create a "dummy" or "automation" Gmail account.
# 2. Fill in the user and password variables below with the credentials from step 1.
# 3. Run this script in a terminal and leave it running until step 7 is completed.
# 3A. You will probably get a SASL error (or similar) the first time you try to run this script. If so:
#     Log into your dummy GMail account, and an email should show up letting you "enable less-secure apps" in your preferences.
#     It might take a minute for the change to take effect.
# 4. Log into your "main" Gmail account - NOT the one created in step 1.
# 5. Send a chat to your dummy account.
# 6. Now look in your terminal. This script should have printed out the "masked" address used by GChat.
# 7. Copy the masked address into the blah variable in xmpp.py
# Note: This process seems to work regardless of if your main Gmail account is signed into the
# "old style chat" or Hangouts.

import xmpp

user = "your_dummy_account@gmail.com"
password = "your_password"
server = ("talk.google.com", 5223)

def message_handler(connect_object, message_node):
    print "Message received from: {}".format(message_node.getFrom())
    message = "This is an automation message"
    connect_object.send(xmpp.Message(message_node.getFrom(), message, typ="chat"))

jid = xmpp.JID(user)
connection = xmpp.Client(jid.getDomain(), debug=[])
connection.connect(server)
result = connection.auth(jid.getNode(), password)

connection.RegisterHandler("message", message_handler)
connection.sendInitPresence()

while connection.Process(1):
    pass