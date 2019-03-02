class TimeZoneDBPlugin(object):

	def __init__(self, config):
		super(TimeZoneDBPlugin, self).__init__()
		self.config = config

	def generate(self, intent, entities, result):

		datetime = result["datetime"]
		location = result["location"]

		return {
			"text": "It is {} in {}".format(datetime, location),
			"voice": "It is {} in {}".format(datetime, location)
		}