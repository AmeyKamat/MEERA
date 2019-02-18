import requests

class NewsAPIPlugin(object):

	def __init__(self, config):
		super(NewsAPIPlugin, self).__init__()
		self.config = config

	def execute(self, message, intent, entities):
		if "query" in entities:
			response = requests.get(self.config["news_url"], params = {
				'q': entities["query"],
				'apiKey': self.config["key"]
			})
		else:
			response = requests.get(self.config["headlines_url"], params= {
				'country': 'in',
				'apiKey': self.config["key"]
			})

		return response.json()["articles"]

	
		