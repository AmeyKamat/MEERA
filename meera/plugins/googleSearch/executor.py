import urllib

class GoogleSearchPlugin(object):

	def __init__(self, config):
		super(GoogleSearchPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		message = context.message
		entities = context.nlpAnalysis.entities
		
		if "query" in entities:
	 		searchQuery = entities["query"]
		else:
			searchQuery = message

		result = {}

		result["url"] = self.config["search_api"] + urllib.request.pathname2url(searchQuery)
	
		return result