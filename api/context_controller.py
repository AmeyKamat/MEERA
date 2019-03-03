import json
from copy import deepcopy

from circuits.web import Controller

from util import jsonDefault

class ContextController(Controller):

	channel = "/context"

	def __init__(self, contextManager):
		super(ContextController, self).__init__()
		self.contextManager = contextManager

	def index(self, contextId):
		context = deepcopy(self.contextManager.getContext(contextId))

		if context.previousContext is not None:
			context.previousContext = context.previousContext.contextId
		
		return json.dumps(context, default=jsonDefault, indent=4)