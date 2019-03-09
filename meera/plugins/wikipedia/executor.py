import urllib

class WikipediaPlugin(object):

	def __init__(self, config):
		super(WikipediaPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities

		searchQuery = entities["query"]
		result = {}
		result["url"] = self.config["wikipedia_api"] + urllib.request.pathname2url(searchQuery)
		return result