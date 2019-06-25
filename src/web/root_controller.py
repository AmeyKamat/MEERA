import os
from circuits.web import Controller

from definitions import PROJECT_DIR

class Root(Controller):

    def index(self):
        return "MEERA"
