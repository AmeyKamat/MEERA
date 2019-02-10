import uuid
from copy import deepcopy
from connection.client import Client

class ClientManager(object):
	
	def __init__(self):
		self.idSocketMapping = {}
		self.clientNames = {}
		self.clientIds = {}
		self.types = {
			"mobile_app": [],
			"web_app": [],
			"telegram_bot": []
		}

	def getByName(self, clientName):
		return deepcopy(self.clientNames[clientName])

	def getById(self, clientId):
		return deepcopy(self.clientIds[clientId])

	def getByDeviceType(self, deviceType):
		return deepcopy(self.types[deviceType])

	def getRegisteredClients(self):
		return deepcopy(list(self.clientIds.values()))

	def getSocket(self, clientId):
		return self.idSocketMapping[clientId]

	def registerClient(self, socket, request):
		client = self.createClient(request)

		if socket not in self.idSocketMapping.values():
			self.clientNames[client.name] = client
			self.clientIds[client.id] = client
			self.types[client.type].append(client)
			self.idSocketMapping[client.id] = socket
			return client
		else:
			raise Exception("client already registered")

	def unregisterDisconnectedClients(self):
		for clientId, socket in list(self.idSocketMapping.items()):
			print(socket is None)
			if socket is None or socket.fileno() == -1:
				client = self.clientIds[clientId]
				self.clientNames.pop(client.name)
				self.clientIds.pop(client.id)
				self.idSocketMapping.pop(client.id)
				self.types[client.type].remove(client)
				return client

	def validateClient(self, clientId):
		return clientId in self.idSocketMapping.keys()

	def createClient(self, request):
		clientId = str(uuid.uuid4())
		return Client(clientId, request["name"], request["deviceType"])