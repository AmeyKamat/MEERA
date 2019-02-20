class ICanHazDadJokePlugin(object):

	def __init__(self, config):
		super(ICanHazDadJokePlugin, self).__init__()
		self.config = config

	def generate(self, intent, entities, result):

		return {
			"text": result["joke"],
			"voice": result["joke"]
		}