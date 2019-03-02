class BarclaycardUSPlugin(object):

	def __init__(self, config):
		super(BarclaycardUSPlugin, self).__init__()
		self.config = config

	def generate(self, intent, entities, result):
		url = result["url"]
		text = "Here is your barclaycard application page.\n\n{0}".format(url)
		voice = "Here is your barclaycard application page.\n\n{0}".format(url)

		return {
			"text": text,
			"voice": voice
		}