import uuid
from copy import deepcopy

from context.model import Context

class ContextManager:

    def __init__(self):
        self.conversations = {}
        self.contexts = {}

    def get_context(self, context_id):
        return self.contexts.get(context_id)

    def get_contexts(self):
        return deepcopy(self.contexts)

    def create_context(self, request):
        client_id = request["body"]['client_id']
        message = request["body"]['message']
        context = Context(client_id, message)
        self.contexts[context.context_id] = context

        conversation_id = request.get('conversation_id')
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
            context.conversation_id = conversation_id
            self.conversations[conversation_id] = context
        else:
            previous_context = self.conversations[conversation_id]
            context.previous_context = previous_context
            self.conversations[conversation_id] = context

        return context

    def clear_conversation(self, conversation_id):
        if conversation_id in self.conversations.keys():
            context = self.conversations[conversation_id]
            self.conversations.pop(conversation_id)

            while context is not None:
                self.contexts.pop(context.context_id)
                context = context.previous_context
        else:
            raise Exception("Conversation not found.")

    def get_conversations(self):
        return deepcopy(self.conversations)
