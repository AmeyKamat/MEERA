import requests

class SayPlugin(object):

	def __init__(self, config):
		super(SayPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities

		result ={}
		result["query"] = entities["query"]
		return result

	
		