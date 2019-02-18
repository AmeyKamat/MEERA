import uuid
from copy import deepcopy
from context.model import Context

class ContextManager(object):
	
	def __init__(self):
		self.conversations = {}
		self.contexts = {}

	def getContext(self, contextId):
		return self.contexts[contextId]

	def createContext(self, request):
		clientId = request["body"]['clientId']
		message = request["body"]['message']
		context = Context(clientId, message)
		self.contexts[context.contextId] = context

		conversationId = request.get('conversationId')
		if conversationId is None:
			conversationId = str(uuid.uuid4())
			context.conversationId = conversationId
			self.conversations[conversationId] = context
		else:
			previousContext = self.conversations[conversationId]
			context.previousContext = previousContext
			self.conversations[conversationId] = context

		return context


	def clearConversation(self, conversationId):
		if conversationId in self.conversations.keys():
			context = self.conversations[conversationId]
			self.conversations.pop(conversationId)

			while context is not None:
				self.contexts.pop(context.contextId)
				context = context.previousContext
		else:
			raise Exception("Conversation not found.")


	def getConversations(self):
		return deepcopy(self.conversations)