import requests

class NewsPlugin(object):

	def __init__(self, config):
		super(NewsPlugin, self).__init__()
		self.config = config

	def execute(context):
		entities = context.nlpAnalysis.entities
		if "query" in entities:
			response = requests.get(self.config["news_api"], params = {
				'q': entities["query"],
				'apiKey': self.config["key"]
			})
		else:
			response = requests.get(self.config["headlines_url"], params= {
				'country': 'in',
				'apiKey': self.config["key"]
			})

		articles = response.json()["articles"]
		text = ""
		voice = ""
		for article in articles:
			source = article["source"]["name"]
			headline = article["title"]
			url = article["url"]
			voice = voice + "According to {0}, {1}. ".format(source, headline)
			text = text + "{0}\nSource: {1}\n{2}\n\n".format(headline, source, url)

		voice = voice + "These headlines are powered by News Api.org"
		text = text + "Powered By NewsApi.org"

		return {
			"text": text,
			"voice": voice
		}



	
		