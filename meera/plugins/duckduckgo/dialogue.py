class DuckDuckGoPlugin(object):

	def __init__(self, config):
		super(DuckDuckGoPlugin, self).__init__()
		self.config = config

	def generate(self, result):
		if "url" not in result:
			answer = result["answer"]
			source = result["source"]
			text = "According to {0}, {1}\n\nPowered by DuckDuckGo".format(source, answer)
			voice = "According to {0}, {1} This answer is powered by DuckDuckGo".format(source, answer)
			url = None
		else:
			url = result["url"]
			text = "This is what I found on internet.\n\n{0}".format(url)
			voice = "This is what I found on internet. {0}".format(url)

		return {
			"text": text,
			"voice": voice,
			"link": url
		}