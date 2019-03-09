import uuid
from copy import deepcopy

from client.model import Client

class ClientManager:
    
    def __init__(self):
        self.idSocketMapping = {}
        self.clientNames = {}
        self.clientIds = {}
        self.clientTypes = {
            "mobile_app": [],
            "web_app": [],
            "telegram_bot": []
        }

    def getByName(self, clientName):
        return deepcopy(self.clientNames[clientName])

    def getById(self, clientId):
        return deepcopy(self.clientIds[clientId])

    def getByDeviceType(self, clientType):
        return deepcopy(self.clientTypes[clientType])

    def getRegisteredClients(self):
        return deepcopy(list(self.clientIds.values()))

    def getSocket(self, clientId):
        return self.idSocketMapping[clientId]

    def registerClient(self, socket, request):
        client = createClient(request)

        if socket in self.idSocketMapping.values():
            raise Exception("client already registered")

        self.clientNames[client.clientName] = client
        self.clientIds[client.clientId] = client
        self.clientTypes[client.clientType].append(client)
        self.idSocketMapping[client.clientId] = socket
        return client

    def unregisterDisconnectedClients(self):
        for clientId, socket in list(self.idSocketMapping.items()):
            if socket is None or socket.fileno() == -1:
                client = self.clientIds[clientId]
                self.clientNames.pop(client.clientName)
                self.clientIds.pop(client.clientId)
                self.idSocketMapping.pop(client.clientId)
                self.clientTypes[client.clientType].remove(client)

    def validateClient(self, clientId):
        return clientId in self.idSocketMapping.keys()

def createClient(request):
    clientId = str(uuid.uuid4())
    return Client(clientId, request["body"]["name"], request["body"]["clientType"])