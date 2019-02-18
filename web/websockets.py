import json

from circuits.net.events import write
from circuits import Component, handler

from events import *
from util import jsonDefault

class WSGateway(Component):

	channel="wsserver"

	def __init__(self, clientManager):
		super(WSGateway, self).__init__()
		self.clientManager = clientManager

		self.switcher = {
			"hello": self.hello,
			"message": self.message,
			"self-location": self.selfLocation
		}

	# stream handlers

	def read(self, sock, request):
		parsedRequest = json.loads(request)
		self.switcher[parsedRequest["type"]](sock, parsedRequest)

	def connect(self, sock, host, port):
		print("device connected with host: {} and port {}".format(host, port))

	def disconnect(self, sock):
		self.clientManager.unregisterDisconnectedClients()

	# events handlers

	@handler("DialogueGeneratedEvent")
	def chat(self, context):
		clientId = context.clientId
		socket = self.clientManager.getSocket(clientId)
		type = "reply"
		body = context.interaction
		contextId = context.contextId

		self.fire(write(socket, getResponse(type, contextId, body)))

		
	@handler("SelfLocationRequiredEvent")
	def requireLocation(self, context):
		clientId = context.clientId
		socket = self.clientManager.getSocket(clientId)
		type = "self-location-request"
		body = None
		contextId = context.contextId

		self.fire(write(socket, getResponse(type, contextId, body)))		


	@handler("ClientRegisteredEvent")
	def clientRegistered(self, client):
		clientId = client.id
		socket = self.clientManager.getSocket(clientId)
		type = "registration_success"
		body = client
		contextId = None

		self.fire(write(socket, getResponse(type, contextId, body)))

	# request handlers

	def hello(self, sock, parsedRequest):
		client = self.clientManager.registerClient(sock, parsedRequest)
		self.fire(ClientRegisteredEvent(client))


	def message(self, sock, parsedRequest):
		if self.clientManager.validateClient(parsedRequest["body"]["clientId"]):
			print(parsedRequest)
			self.fire(MessageReceivedEvent(parsedRequest))


	def selfLocation(self, sock, parsedRequest):
		if self.clientManager.validateClient(parsedRequest["body"]["clientId"]):
			print(parsedRequest)
			self.fire(SelfLocationReceivedEvent(parsedRequest))

#utility methods

def getResponse(type, contextId, body):
	response = {
		"type": type,
		"replyTo": contextId,
		"body": body 
	}

	return json.dumps(response, default=jsonDefault)