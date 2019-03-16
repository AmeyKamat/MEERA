import subprocess

import psutil
from circuits.web import JSONController

from api.serializer import convert_to_dict

class StatusController(JSONController):

    channel = "/status"

    def __init__(self, context_manager, client_manager):
        super(StatusController, self).__init__()
        self.context_manager = context_manager
        self.client_manager = client_manager
        self.version = get_version()

    def index(self):
        return convert_to_dict({
            'status': 'UP',
            'release_version': self.version,
            'cpu_utilization': psutil.cpu_percent(None),
            'memory_utilization': psutil.virtual_memory().percent,
            'registered_clients': len(self.client_manager.get_registered_clients()),
            'requests_received': len(self.context_manager.get_contexts()),
            'conversation_handled': len(self.context_manager.get_conversations())
        })

def get_version():
    return str(
        subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'], 
            stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
    ).split("\n")[0]
