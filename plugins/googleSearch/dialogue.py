class GoogleSearchPlugin(object):

	def __init__(self, config):
		super(GoogleSearchPlugin, self).__init__()
		self.config = config

	def generate(self, result):
		url = result["url"]
		text = "This is what I found on internet.\n\n{0}".format(url)
		voice = "This is what I found on internet."

		return {
			"text": text,
			"voice": voice,
			"link": url
		}