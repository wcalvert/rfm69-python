from yapsy.IPlugin import IPlugin

class FirebasePlugin(IPlugin):
    def __init__(self):
        pass
        
    def process_message(self):
        print "This is the firebase plugin"