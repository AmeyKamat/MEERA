import os

import requests

class NewsAPIPlugin(object):

	def __init__(self, config):
		super(NewsAPIPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities

		key_variable = self.config['key_variable']
		key = os.environ[key_variable]
		
		if "query" in entities:
			response = requests.get(self.config["news_url"], params = {
				'q': entities["query"],
				'apiKey': key
			})
		else:
			response = requests.get(self.config["headlines_url"], params= {
				'country': 'in',
				'apiKey': key
			})

		return response.json()["articles"]

	
		