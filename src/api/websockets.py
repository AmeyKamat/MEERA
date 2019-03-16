import json

from circuits.net.events import write
from circuits import Component, handler

from events import ClientRegisteredEvent, MessageReceivedEvent, SelfLocationReceivedEvent
from api.serializer import serialize

class WSGateway(Component):

    channel = "wsserver"

    def __init__(self, client_manager):
        super(WSGateway, self).__init__()
        self.client_manager = client_manager

        self.switcher = {
            "hello": self.hello,
            "message": self.message,
            "self-location": self.self_location
        }

    # stream handlers

    def read(self, socket, request):
        parsed_request = json.loads(request)
        self.switcher[parsed_request["type"]](socket, parsed_request)

    # pylint: disable=unused-argument,no-self-use
    def connect(self, socket, host, port):
        print("device connected with host: {} and port {}".format(host, port))

    # pylint: disable=unused-argument
    def disconnect(self, socket):
        self.client_manager.unregister_disconnected_clients()

    # events handlers

    @handler("DialogueGeneratedEvent")
    def chat(self, context):
        client_id = context.client_id
        socket = self.client_manager.get_socket(client_id)
        message_type = "reply"
        body = context.interaction
        context_id = context.context_id

        self.fire(write(socket, get_response(message_type, context_id, body)))

    @handler("SelfLocationRequiredEvent")
    def require_location(self, context):
        client_id = context.client_id
        socket = self.client_manager.get_socket(client_id)
        message_type = "self-location-request"
        body = None
        context_id = context.context_id

        self.fire(write(socket, get_response(message_type, context_id, body)))

    @handler("ClientRegisteredEvent")
    def client_registered(self, client):
        client_id = client.client_id
        socket = self.client_manager.get_socket(client_id)
        message_type = "registration-success"
        body = client
        context_id = None

        self.fire(write(socket, get_response(message_type, context_id, body)))

    # request handlers

    def hello(self, sock, parsed_request):
        client = self.client_manager.register_client(sock, parsed_request)
        self.fire(ClientRegisteredEvent(client))

    # pylint: disable=unused-argument
    def message(self, sock, parsed_request):
        print(parsed_request)
        if self.client_manager.validate_client(parsed_request["body"]["client_id"]):
            self.fire(MessageReceivedEvent(parsed_request))

    # pylint: disable=unused-argument
    def self_location(self, sock, parsed_request):
        if self.client_manager.validate_client(parsed_request["body"]["client_id"]):
            self.fire(SelfLocationReceivedEvent(parsed_request))

#utility methods

def get_response(message_type, context_id, body):
    response = {
        "type": message_type,
        "reply_to": context_id,
        "body": body
    }

    return json.dumps(response, default=serialize)
