import json

from circuits.net.events import write
from circuits import Component, handler

from events import MessageReceivedEvent

class WSGateway(Component):

	channel="wsserver"

	def __init__(self, clientManager):
		super(WSGateway, self).__init__()
		self.clientManager = clientManager

		self.switcher = {
			"hello": self.hello,
			"message": self.message
		}

	def read(self, sock, request):
		parsedRequest = json.loads(request)
		self.switcher[parsedRequest["type"]](sock, parsedRequest)

	def connect(self, sock, host, port):
		print("device connected with host: {} and port {}".format(host, port))

	def disconnect(self, sock):
		self.clientManager.unregisterDisconnectedClients()

	@handler("DialogueGeneratedEvent")
	def chat(self, context):
		socket = self.clientManager.getSocket(context.clientId)
		self.fire(write(socket, json.dumps(context.interaction)))

	def hello(self, sock, parsedRequest):
		client = self.clientManager.registerClient(sock, parsedRequest)
		self.fire(write(sock, json.dumps(client.__dict__)))

	def message(self, sock, parsedRequest):
		if self.clientManager.validateClient(parsedRequest["clientId"]):
			print(parsedRequest)
			self.fire(MessageReceivedEvent(parsedRequest))
		else:
			self.fire(write(sock, "Unknown Client: Say hello to MEERA first!"))
			raise Exception("Unknown Client {}: Say hello to MEERA first!".format(parsedRequest.clientId))

