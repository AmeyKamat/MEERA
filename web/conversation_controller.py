import json

from circuits.web import Controller

class ConversationController(Controller):

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

		return json.dumps(formattedConversations, default= lambda o: o.__dict__, indent=4)

def getContextIdList(initialContext):
	context = initialContext
	contextIds = []
	while context is not None:
		contextIds.append(context.contextId)
		context = context.previousContext

	return contextIds