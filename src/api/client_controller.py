from circuits.web import JSONController

from api.serializer import convert_to_dict, serialize

class ClientController(JSONController):

    channel = "/clients"

    def __init__(self, client_manager):
        super(ClientController, self).__init__()
        self.client_manager = client_manager

    def index(self):
        return convert_to_dict(
            list(map(serialize, self.client_manager.get_registered_clients())))
