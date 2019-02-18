import json

from circuits.web import Controller

from util import jsonDefault

class ClientController(Controller):

	channel = "/clients"

	def __init__(self, clientManager):
		super(ClientController, self).__init__()
		self.clientManager = clientManager

	def index(self):
		return json.dumps(
			list(map(jsonDefault, self.clientManager.getRegisteredClients())))
