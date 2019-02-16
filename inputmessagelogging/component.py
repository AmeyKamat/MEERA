from datetime import datetime 
import json

from circuits import Component, handler

class InputMessageLoggingComponent(Component):

	@handler("DialogueGeneratedEvent")
	def logContext(self, context):
		with open("log/meera.log", "a") as log:
			log.write("{0} {1}: Context: {2}\n".format(datetime.now(), context.message, json.dumps(context, default= lambda o: o.__dict__)))