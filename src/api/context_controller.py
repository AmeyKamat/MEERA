from copy import deepcopy

from circuits.web import JSONController

from api.serializer import convert_to_dict

class ContextController(JSONController):

    channel = "/context"

    def __init__(self, context_manager):
        super(ContextController, self).__init__()
        self.context_manager = context_manager

    def index(self, context_id):
        context = deepcopy(self.context_manager.get_context(context_id))

        if context is None:
            return self.notfound("context does not exist")

        if context.previous_context is not None:
            context.previous_context = context.previous_context.context_id

        return convert_to_dict(context)
