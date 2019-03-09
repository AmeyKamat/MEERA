import requests
import urllib

from execution.exception import SelfLocationNotFoundException

class ICanHazDadJokePlugin(object):

	def __init__(self, config):
		super(ICanHazDadJokePlugin, self).__init__()
		self.config = config

	def execute(self, context):
		response = requests.get(self.config["joke_url"], headers = {
				"User-Agent": self.config["user_agent"],
				"accept": "application/json"
			}).json()

		result = {}
		result["joke"] = response["joke"]
		return result