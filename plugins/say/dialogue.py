class SayPlugin(object):

	def __init__(self, config):
		super(SayPlugin, self).__init__()
		self.config = config

	def generate(self, intent, entities, result):

		return {
			"text": entities["query"],
			"voice": entities["query"]
		}