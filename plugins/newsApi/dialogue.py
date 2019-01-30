class NewsPlugin(object):

	def __init__(self, config):
		super(NewsPlugin, self).__init__()
		self.config = config

	def generate(intent, entities, result):
		text = "Here are the headlines.\n\n"
		voice = "Here are the headlines. "
		for article in result:
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