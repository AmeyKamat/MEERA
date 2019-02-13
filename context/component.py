from circuits import Component, handler

from context.model import Context
from events import ContextCreatedEvent

class ContextComponent(Component):

	def __init__(self, contextManager):
		super(ContextComponent, self).__init__()
		self.contextManager = contextManager

	@handler("MessageReceivedEvent")
	def recordContext(self, request):
		context = self.contextManager.createContext(request)
		print("Context created: " + str(context.contextId))
		self.fire(ContextCreatedEvent(context))