import os

import requests
import urllib

from execution.exception import SelfLocationNotFoundException

class GoogleSelfLocationPlugin(object):

	def __init__(self, config):
		super(GoogleSelfLocationPlugin, self).__init__()
		self.config = config

	def execute(self, context):
		entities = context.nlpAnalysis.entities
		
		if "self-location" not in entities:
			raise SelfLocationNotFoundException("Self Location Not Found")
		else:
			selfLocation = entities["self-location"]

			key_variable = self.config['key_variable']
			key = os.environ[key_variable]

			response = requests.get(self.config["geocoding_url"], params= {
				'latlng': str(selfLocation["latitude"]) + "," + str(selfLocation["longitude"]),
	    		'key': key
			}).json()

			result = {}
			result["location"] = response["results"][0]["formatted_address"]

			return result