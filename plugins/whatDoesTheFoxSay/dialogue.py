class WhatDoesTheFoxSayPlugin(object):

	def __init__(self, config):
		super(WhatDoesTheFoxSayPlugin, self).__init__()
		self.config = config

	def generate(self, intent, entities, result):

		return {
			"text": result["response"],
			"voice": result["response"]
		}