# **********************************************************************************
# Wes Calvert, 2015
# **********************************************************************************
# License
# **********************************************************************************
# This program is free software; you can redistribute it 
# and/or modify it under the terms of the GNU General    
# Public License as published by the Free Software       
# Foundation; either version 2 of the License, or        
# (at your option) any later version.                    
#                                                        
# This program is distributed in the hope that it will   
# be useful, but WITHOUT ANY WARRANTY; without even the  
# implied warranty of MERCHANTABILITY or FITNESS FOR A   
# PARTICULAR PURPOSE.  See the GNU General Public        
# License for more details.                              
#                                                        
# You should have received a copy of the GNU General    
# Public License along with this program; if not, write 
# to the Free Software Foundation, Inc.,                
# 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#                                                        
# Licence can be viewed at                               
# http:#www.fsf.org/licenses/gpl.txt                    
#
# Please maintain this license information along with authorship
# and copyright notices in any redistribution of this code
# **********************************************************************************

# This class serves as an interface definition for any radio or simulator.

class BaseRadio(object):

	def __init__(self):
		pass

	def initialize(self, freqBand, nodeId, networkID):
		raise NotImplementedError

	def sleep(self):
		raise NotImplementedError

	def setAddress(self, addr):
		raise NotImplementedError

	def setNetwork(self, networkID):
		raise NotImplementedError

	def setPowerLevel(self, powerLevel):
		raise NotImplementedError

	def send(self, toAddress, buffer, bufferSize, requestACK):
		raise NotImplementedError

	def sendWithRetry(self, toAddress, buffer, bufferSize, retries=2, retryWaitTime=40):
		raise NotImplementedError

	def ACKReceived(self, fromNodeID):
		raise NotImplementedError 

	def ACKRequested(self):
		raise NotImplementedError

	def sendACK(self, buffer="", bufferSize=0):
		raise NotImplementedError

	def receiveDone(self):
		raise NotImplementedError

	def setEncryptionKey(self, key):
		raise NotImplementedError
