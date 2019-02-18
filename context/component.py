from circuits import Component, handler

from context.model import Context
from events import *

class ContextComponent(Component):

	def __init__(self, contextManager):
		super(ContextComponent, self).__init__()
		self.contextManager = contextManager

	@handler("MessageReceivedEvent")
	def recordContext(self, request):
		print(request)
		context = self.contextManager.createContext(request)
		print("Context created: " + str(context.contextId))
		self.fire(ContextCreatedEvent(context))


	@handler("SelfLocationReceivedEvent")
	def updateSelfLocationInContext(self, request):
		contextId = request["contextId"]
		context = self.contextManager.getContext(contextId)
		entities = context.nlpAnalysis.entities

		entities["self-location"] = {
			"latitude": request["body"]["latitude"],
			"longitude": request["body"]["longitude"]
		}

		self.fire(EntitiesPreprocessedEvent(context))