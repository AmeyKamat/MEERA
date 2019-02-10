from circuits import Component, handler

from context.model import Context
from events import ContextCreatedEvent

class ContextComponent(Component):

	recordedContexts = []

	@handler("MessageReceivedEvent")
	def recordContext(self, request):
		context = Context(request["clientId"], request["message"])

		self.recordedContexts.append(context)
		print("Context created: " + str(context))
		
		self.fire(ContextCreatedEvent(context))