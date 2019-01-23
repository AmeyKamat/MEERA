from circuits.net.events import write
from circuits import Component, handler

from events import MessageReceivedEvent

class WSGateway(Component):

	channel="wsserver"

	connections = {}

	def read(self, sock, message):
		print(message)
		self.fire(MessageReceivedEvent(message))

	def connect(self, sock, host, port):
		self.socket = sock

	def disconnect(self, sock):
		self.socket = None