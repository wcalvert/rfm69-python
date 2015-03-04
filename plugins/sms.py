from yapsy.IPlugin import IPlugin

class SmsPlugin(IPlugin):
    def __init__(self):
        pass
        
    def process_message(self):
        print "This is the sms plugin"