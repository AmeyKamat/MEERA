import uuid
from copy import deepcopy

from client.model import Client

class ClientManager:

    def __init__(self):
        self.sockets = {}
        self.client_names = {}
        self.client_ids = {}
        self.client_types = {
            "mobile_app": [],
            "web_app": [],
            "telegram_bot": []
        }

    def get_by_name(self, client_name):
        return deepcopy(self.client_names[client_name])

    def get_by_id(self, client_id):
        return deepcopy(self.client_ids[client_id])

    def get_by_device_type(self, client_type):
        return deepcopy(self.client_types[client_type])

    def get_registered_clients(self):
        return deepcopy(list(self.client_ids.values()))

    def get_socket(self, client_id):
        return self.sockets[client_id]

    def register_client(self, socket, request):
        client = create_client(request)

        if socket in self.sockets.values():
            raise Exception("client already registered")

        self.client_names[client.client_name] = client
        self.client_ids[client.client_id] = client
        self.client_types[client.client_type].append(client)
        self.sockets[client.client_id] = socket
        return client

    def unregister_disconnected_clients(self):
        for client_id, socket in list(self.sockets.items()):
            if socket is None or socket.fileno() == -1:
                client = self.client_ids[client_id]
                self.client_names.pop(client.client_name)
                self.client_ids.pop(client.client_id)
                self.sockets.pop(client.client_id)
                self.client_types[client.client_type].remove(client)

    def validate_client(self, client_id):
        return client_id in self.sockets.keys()

def create_client(request):
    client_id = str(uuid.uuid4())
    return Client(client_id, request["body"]["name"], request["body"]["client_type"])
