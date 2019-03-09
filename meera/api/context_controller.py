import json
from copy import deepcopy

from circuits.web import JSONController

from api.serializer import serializer

class ContextController(JSONController):

    channel = "/context"

    def __init__(self, contextManager):
        super(ContextController, self).__init__()
        self.contextManager = contextManager

    def index(self, contextId):
        context = deepcopy(self.contextManager.getContext(contextId))

        if context.previousContext is not None:
            context.previousContext = context.previousContext.contextId
        
        return json.dumps(context, default=serializer, indent=4)
