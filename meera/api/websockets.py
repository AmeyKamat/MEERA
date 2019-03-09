import json

from circuits.net.events import write
from circuits import Component, handler

from events import ClientRegisteredEvent, MessageReceivedEvent, SelfLocationReceivedEvent
from api.serializer import serializer

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

    # pylint: disable=unused-argument,no-self-use
    def connect(self, sock, host, port):
        print("device connected with host: {} and port {}".format(host, port))

    # pylint: disable=unused-argument
    def disconnect(self, sock):
        self.clientManager.unregisterDisconnectedClients()

    # events handlers

    @handler("DialogueGeneratedEvent")
    def chat(self, context):
        clientId = context.clientId
        socket = self.clientManager.getSocket(clientId)
        messageType = "reply"
        body = context.interaction
        contextId = context.contextId

        self.fire(write(socket, getResponse(messageType, contextId, body)))

        
    @handler("SelfLocationRequiredEvent")
    def requireLocation(self, context):
        clientId = context.clientId
        socket = self.clientManager.getSocket(clientId)
        messageType = "self-location-request"
        body = None
        contextId = context.contextId

        self.fire(write(socket, getResponse(messageType, contextId, body)))        


    @handler("ClientRegisteredEvent")
    def clientRegistered(self, client):
        clientId = client.clientId
        socket = self.clientManager.getSocket(clientId)
        messageType = "registration_success"
        body = client
        contextId = None

        self.fire(write(socket, getResponse(messageType, contextId, body)))

    # request handlers

    def hello(self, sock, parsedRequest):
        client = self.clientManager.registerClient(sock, parsedRequest)
        self.fire(ClientRegisteredEvent(client))

    # pylint: disable=unused-argument
    def message(self, sock, parsedRequest):
        if self.clientManager.validateClient(parsedRequest["body"]["clientId"]):
            print(parsedRequest)
            self.fire(MessageReceivedEvent(parsedRequest))

    # pylint: disable=unused-argument
    def selfLocation(self, sock, parsedRequest):
        if self.clientManager.validateClient(parsedRequest["body"]["clientId"]):
            print(parsedRequest)
            self.fire(SelfLocationReceivedEvent(parsedRequest))

#utility methods

def getResponse(messageType, contextId, body):
    response = {
        "type": messageType,
        "replyTo": contextId,
        "body": body 
    }

    return json.dumps(response, default=serializer)