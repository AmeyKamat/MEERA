import os
import subprocess

from configparser import ConfigParser
import psutil

from circuits.web import JSONController

from api.serializer import convert_to_dict
from definitions import PROJECT_DIR

class StatusController(JSONController):

    channel = "/status"



    def __init__(self, context_manager, client_manager):
        super(StatusController, self).__init__()
        self.context_manager = context_manager
        self.client_manager = client_manager
        self.config = ConfigParser()
        self.config.read(os.path.join(PROJECT_DIR, 'pkg_info.ini'))

    def index(self):
        return convert_to_dict({
            'status': 'UP',
            'release_version': self.config['MEERA']['version'],
            'author': self.config['MEERA']['author'],
            'email': self.config['MEERA']['email'],
            'website': self.config['MEERA']['website'],
            'cpu_utilization': psutil.cpu_percent(None),
            'memory_utilization': psutil.virtual_memory().percent,
            'registered_clients': len(self.client_manager.get_registered_clients()),
            'requests_received': len(self.context_manager.get_contexts()),
            'conversation_handled': len(self.context_manager.get_conversations())
        })
