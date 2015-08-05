from automation_pb2 import *

# magic number to ident our protobuf messages
MAGIC_NUM = 0xfaf

class BaseMessage(object):
	def __init__(self):
		self.m = automation_message()
		self.m.ident = MAGIC_NUM
	def serialize(self):
		return self.m.SerializeToString()

class Heartbeat(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.HEARTBEAT
	def __str__(self):
		return "Heartbeat"

class ProximityDetected(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.PROXIMITY_DETECTED
	def __str__(self):
		return "Proximity Detected"

class MotionDetected(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.MOTION_DETECTED
	def __str__(self):
		return "Motion Detected"

class SoundDetected(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.SOUND_DETECTED
	def __str__(self):
		return "Sound Detected"

class SmokeDetected(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.SMOKE_DETECTED
	def __str__(self):
		return "Smoke Detected"

class OccupancyDetected(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.OCCUPANCY_DETECTED
	def __str__(self):
		return "Occupancy Detected"

class DoorOpened(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.DOOR_OPENED
	def __str__(self):
		return "Door Opened"

class DoorClosed(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.DOOR_CLOSED
	def __str__(self):
		return "Door Closed"

class WindowOpened(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.WINDOW_OPENED
	def __str__(self):
		return "Window Opened"

class WindowClosed(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.WINDOW_CLOSED
	def __str__(self):
		return "Window Closed"

class LightTurnedOn(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.LIGHT_TURNED_ON
	def __str__(self):
		return "Light Turned On"

class LightTurnedOff(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.LIGHT_TURNED_OFF
	def __str__(self):
		return "Light Turned Off"

class ApplianceTurnedOn(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.APPLIANCE_TURNED_ON
	def __str__(self):
		return "Appliance Turned On"

class ApplianceTurnedOff(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.APPLIANCE_TURNED_OFF
	def __str__(self):
		return "Appliance Turned Off"

class CredentialsAccepted(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.CREDENTIALS_ACCEPTED
	def __str__(self):
		return "Credentials Accepted"

class CredentialsRejected(BaseMessage):
	def __init__(self):
		BaseMessage.__init__(self)
		self.m.type = automation_message.EVENT
		self.m.event_type = automation_message.CREDENTIALS_REJECTED
	def __str__(self):
		return "Credentials Rejected"

