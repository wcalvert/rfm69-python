from yapsy.IPlugin import IPlugin

class EmailPlugin(IPlugin):
    def __init__(self):
        pass
        
    def process_message(self):
        print "This is the email plugin"