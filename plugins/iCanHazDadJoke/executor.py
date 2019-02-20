import requests
import urllib

from execution.exception import SelfLocationNotFoundException

class ICanHazDadJokePlugin(object):

	def __init__(self, config):
		super(ICanHazDadJokePlugin, self).__init__()
		self.config = config

	def execute(self, message, intent, entities):
		response = requests.get(self.config["jokes_url"], headers = {
				"User-Agent": self.config["user_agent"]
			}).json()

		result = {}
		result["joke"] = response["joke"]
		return result