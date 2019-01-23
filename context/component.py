from circuits import Component, handler

from context.model import Context
from events import ContextCreatedEvent

class ContextComponent(Component):

	recordedContexts = []

	@handler("MessageReceivedEvent")
	def recordContext(self, message):
		context = Context(message)

		self.recordedContexts.append(context)
		print("Context created: " + str(context))
		
		self.fire(ContextCreatedEvent(context))