import json

from circuits.web import JSONController

from api.serializer import serializer

class ConversationController(JSONController):

    channel = "/conversations"

    def __init__(self, contextManager):
        super(ConversationController, self).__init__()
        self.contextManager = contextManager

    def index(self):
        conversations = self.contextManager.getConversations()
        formattedConversations = []
        for initialContext in conversations.values():
            formattedConversations.append({
                "conversationId": initialContext.conversationId,
                "contexts": getContextIdList(initialContext)
            })

        return json.dumps(formattedConversations, default=serializer)

def getContextIdList(initialContext):
    context = initialContext
    contextIds = []
    while context is not None:
        contextIds.append(context.contextId)
        context = context.previousContext

    return contextIds