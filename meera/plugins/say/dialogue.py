class SayPlugin(object):

	def __init__(self, config):
		super(SayPlugin, self).__init__()
		self.config = config

	def generate(self, result):

		return {
			"text": result["query"],
			"voice": result["query"]
		}