class ICanHazDadJokePlugin(object):

	def __init__(self, config):
		super(ICanHazDadJokePlugin, self).__init__()
		self.config = config

	def generate(self, result):

		return {
			"text": result["joke"],
			"voice": result["joke"]
		}