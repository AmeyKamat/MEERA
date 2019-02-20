import random

class WhatDoesTheFoxSayPlugin(object):

	def __init__(self, config):
		super(SayPlugin, self).__init__()
		self.config = config
		self.foxSounds = [
			"Ring-ding-ding-ding-dingeringeding!",
			"Wa-pa-pa-pa-pa-pa-pow!",
			"Hatee-hatee-hatee-ho!",
			"Joff-tchoff-tchoffo-tchoffo-tchoff!",
			"Jacha-chacha-chacha-chow!",
			"Fraka-kaka-kaka-kaka-kow!",
			"A-hee-ahee ha-hee!",
			"A-oo-oo-oo-ooo!"
		]

	def execute(self, message, intent, entities):
		result = {}
		result["response"] = random.choice(self.foxSounds)
		return result