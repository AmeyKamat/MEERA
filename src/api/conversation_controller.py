from circuits.web import JSONController

from api.serializer import convert_to_dict

class ConversationController(JSONController):

    channel = "/conversations"

    def __init__(self, context_manager):
        super(ConversationController, self).__init__()
        self.context_manager = context_manager

    def index(self):
        conversations = self.context_manager.get_conversations()
        formatted_conversations = []
        for initial_context in conversations.values():
            formatted_conversations.append({
                "conversation_id": initial_context.conversation_id,
                "contexts": get_context_ids(initial_context)
            })

        return convert_to_dict(formatted_conversations)

def get_context_ids(initial_context):
    context = initial_context
    context_ids = []
    while context is not None:
        context_ids.append(context.context_id)
        context = context.previous_context

    return context_ids
