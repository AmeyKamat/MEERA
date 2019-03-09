import json

from circuits.web import JSONController

from api.serializer import serializer

class ClientController(JSONController):

    channel = "/clients"

    def __init__(self, clientManager):
        super(ClientController, self).__init__()
        self.clientManager = clientManager

    def index(self):
        return json.dumps(
            list(map(serializer, self.clientManager.getRegisteredClients())))
