import json

from circuits.web import Controller

class ClientController(Controller):


	def __init__(self, clientManager):
		super(ClientController, self).__init__()
		self.clientManager = clientManager

	def clients(self):
		return json.dumps(
			list(map(lambda x: x.__dict__, self.clientManager.getRegisteredClients())))
