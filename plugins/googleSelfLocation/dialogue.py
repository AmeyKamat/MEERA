class GoogleSelfLocationPlugin(object):

	def __init__(self, config):
		super(GoogleSelfLocationPlugin, self).__init__()
		self.config = config

	def generate(self, result):

		return {
			"text": "You are at " + result["location"],
			"voice": "You are at " + result["location"]
		}