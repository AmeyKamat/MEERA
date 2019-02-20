import urllib

class WikipediaPlugin(object):

	def __init__(self, config):
		super(WikipediaPlugin, self).__init__()
		self.config = config

	def execute(self, message, intent, entities):
	 	searchQuery = entities["query"]
	 	result["url"] = self.config["wikipedia_api"] + urllib.request.pathname2url(searchQuery)
	 	return result
